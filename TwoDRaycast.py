from Utils import *
from graphic_mansart import *
from math import floor
import pygame

#Vector = Point

pygame.init()

class Entity :
    def __init__(self,x,y,map,angle) :
        self.pos = Vector2D(x,y) #Position du Joueur
        self.angle = angle #Direction où pointe Joueur
        self.dir = rotateVector(Vector2D(1,0),angle*math.pi/180) #Vecteur du directeur par rapport à la direction où pointe Joueur
        self.map = map

    def Move(self,speed) :
        """ Déplacer le joueur selon la distance donnée sur l'axe y :
        Avancer : speed > 0
        Reculer : speed < 0
        """
        self.pos.x += self.dir.x * speed
        self.pos.y += self.dir.y * speed

    def distance(self, Vector) -> float:
        """ Renvoie la distance entre la pos du joueur et le point Vector"""
        return math.sqrt((self.pos.x - Vector.x)**2 + (self.pos.y - Vector.y)**2)


class Player(Entity):
    def __init__(self,fov,angle,x,y,map,window) -> None:
        self.fov = fov #Champ de vision du Joueur
        self.window = window #Fenêtre Graphique
        super().__init__(x,y,map,angle)

    

    def Rotate(self, angle) :
        """ Modifie où pointe le joueur selon l'angle donnée :
        Gauche : angle < 0
        Droite : angle > 0
        """
        self.angle += angle
        self.dir = rotateVector(Vector2D(1,0),self.angle*math.pi/180) #Vecteur du directeur par rapport à la direction où pointe Joueur

    def drawRay(self, Vector) :
        """ Trace une ligne entre la pos du joueur et le point Vector """
        pygame.draw.line(self.window,pygame.Color(0,0,255),(self.pos.x, self.pos.y),(Vector.x,Vector.y),1)



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

            walls += [self.distance(self.findWall(newVector))]
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






def displayAll(map,player : Player,window) :
    """ Affiche tous les éléments du jeu en 2D sur la fenêtre graphique """
    for i in range (len(map)) :
        for j in range (len(map[i])) :
            if map[i][j] == "#" :
                #Si mur : Dessine Cube Noir
                pygame.draw.rect(window,pygame.Color(0,0,0),(480/len(map)*j,480/len(map)*i,int(480/len(map)),int(480/len(map))))
            else :
                # Si en place vide : Dessine Cube Blanc
                pygame.draw.rect(window,pygame.Color(255,255,255),(480/len(map)*j,480/len(map)*i,int(480/len(map)),int(480/len(map))))
    # Place le Joueur à sa position
    pygame.draw.circle(window,pygame.Color(255,0,0),(int(player.pos.x),int(player.pos.y)),5)
    player.drawAllRays()

            

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
            if self.map[cadrey][cadrex] == "#" :

                distancey = math.sqrt((posx - x2)**2 + (posy - y2)**2)
                

        if distancex > distancey :
            return Vector2D(x2,y2)
        else : 
            return Vector2D(x1,y1)
    
    def drawAllRays(self) :
        for i in range(-self.fov//2, self.fov//2) :
            
            angle = i * math.pi/180

            newVector = rotateVector(self.dir,angle)

            self.drawRay(self.findWall(newVector))
            


    


def displayAll(map,player,window) :
    for i in range (len(map)) :
        for j in range (len(map[i])) :
            if map[i][j] == "#" :
                pygame.draw.rect(window,pygame.Color(0,0,0),(480/len(map)*j,480/len(map)*i,int(480/len(map)),int(480/len(map))))
            else :
                pygame.draw.rect(window,pygame.Color(255,255,255),(480/len(map)*j,480/len(map)*i,int(480/len(map)),int(480/len(map))))
    pygame.draw.circle(window,pygame.Color(255,0,0),(int(player.pos.x),int(player.pos.y)),5)
    player.drawAllRays()
    
