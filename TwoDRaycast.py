from dis import dis
from gettext import find
from hashlib import new

from sympy import factor, false, true
from Utils import *
from graphic_mansart import *
import pygame


pygame.init()

class Player :
    def __init__(self,fov,angle,x,y,map,window) -> None:
        self.fov = fov
        self.angle = angle
        self.pos = Vector2D(x,y)
        self.dir = rotateVector(Vector2D(1,0),angle*math.pi/180)
        self.map = map
        self.window = window
    
    def Move(self,speed) :
        self.pos.x += self.dir.x * speed
        self.pos.y += self.dir.y * speed

    def Rotate(self, angle) :
        self.angle += angle
        self.dir = rotateVector(Vector2D(1,0),self.angle*math.pi/180)
    
    def drawRay(self, Vector) :
        pygame.draw.line(self.window,pygame.Color(0,0,255),(self.pos.x, self.pos.y),(Vector.x,Vector.y),1)

    def distance(self, Vector) :
        return math.sqrt((self.pos.x - Vector.x)**2 + (self.pos.y - Vector.y)**2)

    def scanWalls(self) :
        walls = []
        for i in range(-self.fov, self.fov) :
            
            a = i/2
            angle = a * math.pi/180

            newVector = rotateVector(self.dir,angle)

            walls += [self.distance(self.findWall(newVector))]
        return walls

    def findWall(self,Vector) :
        posx = self.pos.x 
        posy = self.pos.y 

        i = 0

        distancex = 0
        distancey = 0

        x1 = 0
        y1 = 0

        x2 = 0
        y2 = 0


        cadrex = floor(posx/ 480 * len(self.map))
        cadrey = floor(posy/ 480 * len(self.map))

        while self.map[cadrey][cadrex] != "#" :

            i += 1
                
            facteurx = floor(posx+i)-posx

            x1 = Vector.x*facteurx+posx
            y1 = Vector.y*facteurx+posy

            cadrex = floor(x1/ 480 * len(self.map))
            cadrey = floor(y1/ 480 * len(self.map))

            if self.map[cadrey][cadrex] == "#" :

                distancex = math.sqrt((posx - x1)**2 + (posy - y1)**2)

            

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
    
