# echap = quit  / resolution fix : height = 1920 / width = 1080

from math import floor
from tracemalloc import start
from matplotlib.pyplot import draw
from numpy import angle
import TwoDRaycast
import pygame
from pygame.locals import *
from dis import dis
from gettext import find
from hashlib import new
from sympy import factor, false, true

height = 1920
width = 1080

class Vector2D :
    def __init__(self,x,y) :
        self.x = x
        self.y = y

def stringToList(map) :
    for i in range (len(map)) :
        map[i] = list(map[i])
    return map

def rotateVector(Vector,angle) :
    x1 = Vector.x
    y1 = Vector.y

    return Vector2D(round(x1*math.cos(angle) - y1*math.sin(angle),5), round(x1*math.sin(angle) + y1*math.cos(angle),5))

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
        for i in range(-self.fov//2, self.fov//2) :

            angle = i * math.pi/180

            newVector = rotateVector(self.dir,angle)

            walls += [self.distance(self.findWall(newVector))*math.cos(angle)]
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


        cadrex = floor(posx/ width * len(self.map))
        cadrey = floor(posy/ width * len(self.map))

        while self.map[cadrey][cadrex] != "#" :

            i += 1

            facteurx = floor(posx+i)-posx

            x1 = Vector.x*facteurx+posx
            y1 = Vector.y*facteurx+posy

            cadrex = floor(x1/ width * len(self.map))
            cadrey = floor(y1/ width * len(self.map))

            if self.map[cadrey][cadrex] == "#" :

                distancex = math.sqrt((posx - x1)**2 + (posy - y1)**2)



        i = 0

        cadrex = floor(posx/ width * len(self.map))
        cadrey = floor(posy/ width * len(self.map))

        while self.map[cadrey][cadrex] != "#" :
            i += 1

            facteurx = floor(posx+i)-posx

            x2 = Vector.x*facteurx+posx
            y2 = Vector.y*facteurx+posy

            cadrex = floor(x2/ width * len(self.map))
            cadrey = floor(y2/ width * len(self.map))
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
                pygame.draw.rect(window,pygame.Color(0,0,0),(width/10*j,width/10*i,int(width/10),int(width/10)))
            else :
                pygame.draw.rect(window,pygame.Color(255,255,255),(width/10*j,width/10*i,int(width/10),int(width/10)))
    pygame.draw.circle(window,pygame.Color(255,0,0),(int(player.pos.x),int(player.pos.y)),5)
    player.drawAllRays()

pygame.init()

window = pygame.display.set_mode((height,width))

class Camera (TwoDRaycast.Player) :
    def __init__(self, fov, angle, x, y, map, window,resolution) -> None:
        super().__init__(fov, angle, x, y, map, window)
        self.resolution = resolution
    def render3D(self, scans) :
        duplicateLines = 1/len(scans)*self.resolution[0]
        for i in range (len(scans)) :
            height = self.GetHeight(scans[i])
            startHeightPoint = Vector2D(i*int(duplicateLines),height[0])
            endHeightPoint = Vector2D(i*int(duplicateLines),height[1])
            color = self.GetBlackTone(scans[i])
            pygame.draw.line(self.window,color,(startHeightPoint.x,startHeightPoint.y),(endHeightPoint.x,endHeightPoint.y),int(duplicateLines))




    def GetHeight(self, distance) :
        halfScreen = self.resolution[1]//2
        height = self.resolution[1]-(distance/width * self.resolution[1])
        StartHeight = halfScreen - height//2
        EndHeight = halfScreen + height//2
        return StartHeight,EndHeight

    def GetBlackTone(self,distance) :
        blacktone = floor(distance/width * 300)
        if blacktone > 255:
            blacktone = 255
        return pygame.Color(255-blacktone,255-blacktone,255-blacktone)


map = stringToList([
    "#############",
    "#           #",
    "#           #",
    "#   ####    #",
    "#     ###   #",
    "#           #",
    "#           #",
    "#           #",
    "#           #",
    "#           #",
    "#           #",
    "#           #",
    "#############"
    ])


player = Camera(60,0,width//2,width//2,map,window,(height,width))

while True :
    for i in pygame.event.get() :
        if i.type == pygame.QUIT :
            pygame.quit()
            exit()
    pygame.display.flip()
    pygame.draw.rect(window,pygame.Color(0,0,0),(0,0,int(height),int(width)),0)
    player.render3D(player.scanWalls())
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] :
        player.Rotate(-5)
    elif keys[pygame.K_RIGHT]:
        player.Rotate(5)
    elif keys[pygame.K_UP]:
        player.Move(5)
    elif keys[pygame.K_DOWN]:
        player.Move(-5)
    elif keys[pygame.K_ESCAPE]:
        pygame.display.quit()
        pygame.quit()
