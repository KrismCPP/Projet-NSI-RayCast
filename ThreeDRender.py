"""Programme Principal du Jeu - Rendu 3D"""

'''IMPORTATION DES MODULES'''

from distutils.spawn import spawn
from math import floor
import re
from tracemalloc import start
from turtle import screensize
from Utils import *
import time
import TwoDRaycast
import pygame
import laby

'''Variables'''

resolutionEcran = [640,480]

'''Classe'''

class Camera (TwoDRaycast.Player) :
    """ Classe Fille de Player """
    def __init__(self, fov, angle, x, y, map, window,resolution) -> None:
        super().__init__(fov, angle, x, y, map, window)
        self.resolution = resolution

    def GetHeight(self, distance) :
        """Renvoie selon la distance le point de l'axe y du haut et du bas du mur"""

        halfScreen = self.resolution[1]//2

        if distance == float('inf') :
            return halfScreen,halfScreen

        height = (962//30*self.resolution[1])/distance

        StartHeight = halfScreen - height//2
        EndHeight = halfScreen + height//2

        return StartHeight,EndHeight

    def GetBlackTone(self,distance) :
        """ Renvoie ue nuance de gris du mur selon la distance """
        if distance == float('inf') :
            return 0
        blacktone = floor(distance/self.mapScale * 300)
        if blacktone > 255:
            blacktone = 255
        return 255-blacktone

    def GetPartOfWall(self, point, texture) :
        """ Retourne la partie du mur texturé """
        #Adapte les coordonnés du point pour qu'il soit utilisable
        if point == Vector2D(float('inf'),float('inf')) :
            return texture[0]
        pointModifie = point
        while pointModifie.y >= 48 :
            pointModifie.x -= 48
            pointModifie.y -= 48
        #Trouve la partie de la texture
        part = int(pointModifie.y/48 *len(texture))
        return texture[part]

    def drawTexturedLine(self,point,distance,duplicateLines,texture,partOfScreen) :
        """ Dessine la ligne des textures """
        height = self.GetHeight(distance)
        if height == (self.resolution[1]//2,self.resolution[1]//2) :
            return
        lenHeight = height[1]-height[0]
        line = self.GetPartOfWall(point,texture)
        toDark = self.GetBlackTone(distance)/255
        for i in range (len(line)) :
            startPoint = Vector2D(partOfScreen*int(duplicateLines),i/len(line)*lenHeight+height[0])
            endPoint = Vector2D(partOfScreen*int(duplicateLines),(i+1)/len(line)*lenHeight+height[0])
            pygame.draw.line(self.window,pygame.Color(int(line[i][0]*255*toDark),int(line[i][1]*255*toDark),int(line[i][2]*255*toDark)),(startPoint.x,startPoint.y),(endPoint.x,+endPoint.y),int(duplicateLines))
        #Trouve un point sur l'axe x en l'adaptant à la résolution



    def render3D(self, scans : list) :
        """ scans : scanWalls()
        Permet d'afficher le rendu 3D sur la fenêtre graphique
        """
        #Adapte l'affiche des murs selon la résolution
        duplicateLines = math.ceil(1/len(scans)*self.resolution[0])
        for i in range (len(scans)) :
            self.drawTexturedLine(scans[i][1],scans[i][0],duplicateLines,Wall,i)

''' Main '''

#______________## INITIALISATION DU JEU ##______________#


#Fenetre Graphique
pygame.init()
window = pygame.display.set_mode((resolutionEcran[0],resolutionEcran[1]))

# Map Sous forme de Liste de Liste
laby_genere = laby.generateur_laby(20)
map,spawn = laby_genere[0],laby_genere[1]

# Init du joueur
player = Camera(90,0,spawn.x*48,spawn.y*48,map,window,(resolutionEcran[0],resolutionEcran[1]))

# Init des configurations du Monstre
monstre = TwoDRaycast.Monster(0,(spawn.x*48 ,spawn.y*48),(spawn.y,spawn.x),map,window)
depart = time.time() # Début du chronomètre
monster_arrival_time = 10 # en secondes
nb_dep = 0 # Déplacement du Monstre en fonction du nb de dep du Joueur


#______________## PROGRAMME PRINCIPAL ##______________#

while True :

    # Si l'utilisateur ferme la fenêtre
    for i in pygame.event.get() :
        if i.type == pygame.QUIT :
            pygame.quit()
            exit()

    #Permet d'actualiser la Page
    pygame.display.flip()
    pygame.draw.rect(window,pygame.Color(0,0,0),(0,0,int(resolutionEcran[0]),int(resolutionEcran[1])),0)

    #Lance le Rendu 3D
    player.render3D(player.scanWalls())

    keys = pygame.key.get_pressed()

    ''' TOUCHES ORDINAIRES '''
    # Tourne à gauche
    if keys[pygame.K_q] :
        player.rotate(-10)

    # Tourne à droite
    elif keys[pygame.K_d]:
        player.rotate(10)

    # Avance
    elif keys[pygame.K_z]:
        player.move(5)
        nb_dep += 1

    # Recule
    elif keys[pygame.K_s]:
        player.move(-5)
        nb_dep += 1
    # Lance le Rendu 2D si TAB est appuyée
    elif keys[pygame.K_TAB]:
        TwoDRaycast.displayAll(map,player,monstre,window)



    ''' TOUCHES SOUS PYGAME'''
    """
    # Tourne à gauche
    if keys[pygame.K_a] :
        player.rotate(-10)

    # Tourne à droite
    elif keys[pygame.K_d]:
        player.rotate(10)

    # Avance
    elif keys[pygame.K_w]:
        player.move(5)
        nb_dep += 1

    # Recule
    elif keys[pygame.K_s]:
        player.move(-5)
        nb_dep += 1
    # Lance le Rendu 2D si TAB est appuyée
    elif keys[pygame.K_TAB]:
        TwoDRaycast.displayAll(map,player, monstre ,window)
    """


    # Si le temps "inoffensif" est dépassé
    if time.time() - depart > monster_arrival_time :

        # Tous les 5 déplacements du Joueur, le monstre se déplace
        if nb_dep >= 5 :

            # On cherche le chemin pour atteindre le joueur
            path = monstre.path_finding((player.pos.x,player.pos.y) )
            if not path :
                # Si le Monstre et sur la case du Joueur
                print("GAME OVER")
            else :
                # On déplace la position du Monstre
                monstre.move(path[0])

            # On réinitilise le nombre de déplacement du Joueur
            nb_dep = 0




