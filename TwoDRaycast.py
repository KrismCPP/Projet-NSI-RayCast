"""Rendu 2D - Fonctions et Classes Utiles"""


'''IMPORTATION DES MODULES'''

from asyncio.windows_events import INFINITE
from Utils import *
from graphic_mansart import *
from math import floor
import pygame


'''Classes'''

class Entity :
    def __init__(self,x,y,map,angle,window) :
        self.pos = Vector2D(x,y) #Position du Joueur
        self.angle = angle #Direction où pointe Joueur
        self.dir = rotateVector(Vector2D(1,0),angle*math.pi/180) #Vecteur du directeur par rapport à la direction où pointe Joueur
        self.map = map
        self.window = window

class Player(Entity):
    """ Classe fille de Entity"""
    def __init__(self,fov,angle,x,y,map,window) :
        self.fov = fov #Champ de vision du Joueur
        super().__init__(x,y,map,angle,window)


    def move(self,speed) :
        """ Déplacer le joueur selon la distance donnée sur l'axe y :
        Avancer : speed > 0
        Reculer : speed < 0
        """
        if speed > 0:
            if self.distance(self.findWall(rotateVector(Vector2D(1,0),(self.angle)*math.pi/180))) > 5 :
                self.pos.x += self.dir.x * speed
                self.pos.y += self.dir.y * speed
        if speed < 0:
            if self.distance(self.findWall(rotateVector(Vector2D(-1,0),(self.angle)*math.pi/180))) > 5 :
                self.pos.x += self.dir.x * speed
                self.pos.y += self.dir.y * speed


    def rotate(self, angle) :
        """ Modifie où pointe le joueur selon l'angle donnée :
        Gauche : angle < 0
        Droite : angle > 0
        """
        self.angle += angle
        self.dir = rotateVector(Vector2D(1,0),self.angle*math.pi/180) #Vecteur du directeur par rapport à la direction où pointe Joueur


    def distance(self, Vector) -> float:
        """ Renvoie la distance entre la pos du joueur et le point Vector"""
        if Vector.x == float('inf') and Vector.y == float('inf') :
            return float('inf')
        return math.sqrt((self.pos.x - Vector.x)**2 + (self.pos.y - Vector.y)**2)


    def drawRay(self, Vector) :
        """ Trace une ligne entre la pos du joueur et le point Vector """
        pygame.draw.line(self.window,pygame.Color(0,0,255),(self.pos.x/3, self.pos.y/3),(Vector.x/3,Vector.y/3),1)


    def findWall(self,Vector) :
        """ Prend en argument un Vecteur
        Renvoie le point le plus proche en intersection avec un mur
        """
        posx = self.pos.x
        posy = self.pos.y

        # Variable Distance entre Joueur et pt d'intersection sur l'axe...
        distancex = 0
        distancey = 0

        x1 = 0
        y1 = 0

        x2 = 0
        y2 = 0

        '''Intersection sur l'axe des abscisse'''
        i = 0
        # Obtenir
        cadrex = floor(posx/ 480 * len(self.map))
        cadrey = floor(posy/ 480 * len(self.map))

        while self.map[cadrey][cadrex] != "#" :
            ''' Tant qu'il ne croise pas de mur '''

            i += 1

            # Prolonge la taille du vecteur jusqu'à rencontrer un mur
            facteurx = floor(posx+i)-posx

            x1 = Vector.x*facteurx+posx
            y1 = Vector.y*facteurx+posy

            # Adapte le pt d'intersection aux indice de la map
            cadrex = floor(x1/ 480 * len(self.map))
            cadrey = floor(y1/ 480 * len(self.map))

            if cadrex > len(self.map)-1 or cadrey > len(self.map)-1 :
                return Vector2D(float('inf'),float('inf'))

            # Vérifie si présence de mur à ce pt d'intersection
            if self.map[cadrey][cadrex] == "#" :

                distancex = math.sqrt((posx - x1)**2 + (posy - y1)**2)


        ''' Intersection sur l'axe des ordonnées'''
        i = 0

        cadrex = floor(posx/ 480 * len(self.map))
        cadrey = floor(posy/ 480 * len(self.map))

        while self.map[cadrey][cadrex] != "#" :
            i += 1

            facteurx = floor(posx+i)-posx

            x2 = Vector.x*facteurx+posx
            y2 = Vector.y*facteurx+posy

            cadrex = floor(x2/ 480 * len(self.map))
            cadrey = floor(y2/ 480 * len(self.map))

            if cadrex > len(self.map)-1 or cadrey > len(self.map)-1 :
                return Vector2D(float('inf'),float('inf'))

            if self.map[cadrey][cadrex] == "#" :

                distancey = math.sqrt((posx - x2)**2 + (posy - y2)**2)

        ''' Renvoie le pt d'intersection le plus petit en abscisse et ordonnée'''
        if distancex > distancey :
            return Vector2D(x2,y2)
        else :
            return Vector2D(x1,y1)


    def scanWalls(self) -> list :
        """
        Renvoie la distance des différents murs dans son champ de vision
        sous forme de liste
        """
        walls = []
        for i in range(-self.fov, self.fov) :
            #Balaye son champ de vision entièrement

            angle_deg = i/2
            angle_radius = angle_deg * math.pi/180

            #Pointe vers la valeur i
            newVector = rotateVector(self.dir,angle_radius)

            wallFound = self.findWall(newVector)

            walls += [(self.distance(wallFound),wallFound)]
        return walls


    def drawAllRays(self) :
        """
        Trace les différents vecteurs entre le joueur et les murs
        sur son champ de vision
        """
        for i in range(-self.fov//2, self.fov//2) :

            angle = i * math.pi/180

            newVector = rotateVector(self.dir,angle)

            self.drawRay(self.findWall(newVector))



class Monster (Entity) :
    """ Classe fille de Entity"""

    def __init__(self,angle,pos_graph,pos_list,map,window) :
        self.pos_list = pos_list
        super().__init__(pos_graph[0],pos_graph[1],map,angle,window)

    def move(self, new_pos) :
        """ Prend en argument un tuple
        Déplace l'indice du Monstre à celle indiquée"""
        self.pos_list = new_pos
        self.pos.x,self.pos.y = self.pos_list[1]*48,self.pos_list[0]*48

    def path_finding(self,pos_player):
        """
        Prend en arguement la position du joueur sous forme de tuple
        Renvoie une liste de plusieurs tuple contenant le chemin pour aller jusqu'au joueur
        """
        # Adapte les coordonnées du joueur par rapport a la liste de liste 'map'
        pos_player = (floor(pos_player[1]/ 480 * len(self.map)), floor(pos_player[0]/ 480 * len(self.map)))

        paths_possibilities = [self.pos_list] # Stockera tous les chemins enivisageable au fur et à mesure
        visited = {} #Dictionnaire pour conserver les positions visitées

        while len(paths_possibilities) != 0: # Tant qu'il reste un chemin possible

            # On traite un des chemins possibles
            if paths_possibilities[0] == self.pos_list:
                path = [paths_possibilities.pop(0)]
            else:
                path = paths_possibilities.pop(0)
            x,y = path[-1] # Assigne à x,y les dernières valeurs du chemin en construction

            if (x,y) == pos_player: # Vérifie si ce chemin atteint la destination
                path.pop(0)
                return path

            elif (x,y) not in visited: # Recherche si la position n'est pas encore visitée

                '''Recherche des directions possibles'''
                coord_to_check = [ (x+1,y), (x-1,y), (x,y+1), (x,y-1)] # 4 Directions
                next_pos = list() # Var pour stocker les nouvelles positions possibles
                for next_coord in coord_to_check:
                    if self.map[next_coord[0]][next_coord[1]] != '#' and next_coord not in visited:
                        next_pos.append(next_coord)

                '''Stockage du nouveau chemin avec les autres possibilités'''
                for coord in next_pos:
                    newPath = list(path)
                    newPath.append(coord)
                    paths_possibilities.append(newPath)

                visited[(x,y)] = None # Ajout de cette position à celles déjà visitées



'''Fonctions'''


def displayAll(map,player : Player, monster : Monster,window) :
    """ Affiche tous les éléments du jeu en 2D sur la fenêtre graphique """
    for i in range (len(map)) :
        for j in range (len(map[i])) :
            if map[i][j] == "#" :
                #Si mur : Dessine Cube Noir
                pygame.draw.rect(window,pygame.Color(255,255,255),(480/len(map)/3*j,480/len(map)*i/3,int(480/len(map)/3),int(480/len(map)/3)))
    # Place le Joueur à sa position
    pygame.draw.circle(window,pygame.Color(255,0,0),(int(player.pos.x)/3,int(player.pos.y)/3),5)
    pygame.draw.circle(window,pygame.Color(0,0,255),(int(monster.pos.x/3),int(monster.pos.y/3)),5)


def displayMonsterPlayer(player, monster, window) :
    pygame.draw.circle(window,pygame.Color(255,0,0),(int(player.pos.x/3),int(player.pos.y/3)),5)
    pygame.draw.circle(window,pygame.Color(125,125,125),(int(monster.pos.x/3),int(monster.pos.y/3)),5)

