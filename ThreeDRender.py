from math import floor
from tracemalloc import start

from matplotlib.pyplot import draw
from numpy import angle
import TwoDRaycast
import pygame

from Utils import *


pygame.init()



window = pygame.display.set_mode((1280,962))

class Camera (TwoDRaycast.Player) :
    def __init__(self, fov, angle, x, y, map, window,resolution) -> None:
        super().__init__(fov, angle, x, y, map, window)
        self.resolution = resolution
    def render3D(self, scans) :
        duplicateLines = math.ceil(1/len(scans)*self.resolution[0])
        for i in range (len(scans)) :
            height = self.GetHeight(scans[i])
            startHeightPoint = Vector2D(i*int(duplicateLines),height[0])
            endHeightPoint = Vector2D(i*int(duplicateLines),height[1])
            color = self.GetBlackTone(scans[i])
            pygame.draw.line(self.window,color,(startHeightPoint.x,startHeightPoint.y),(endHeightPoint.x,endHeightPoint.y),int(duplicateLines))
            
    

    
    def GetHeight(self, distance) :
        halfScreen = self.resolution[1]//2
        height = (962//30*self.resolution[1])/distance
        if height > self.resolution[1] :
            height = self.resolution[1]
        StartHeight = halfScreen - height//2
        EndHeight = halfScreen + height//2
        return StartHeight,EndHeight

    def GetBlackTone(self,distance) :
        blacktone = floor(distance/480 * 300)
        if blacktone > 255:
            blacktone = 255
        return pygame.Color(255-blacktone,255-blacktone,255-blacktone)


map = stringToList([
    "#############",
    "#   #       #",
    "#   #  ##   #",
    "#  #####    #",
    "#  #   #    #",
    "#  #   ###  #",
    "#    #  #   #",
    "#    ####   #",
    "#    #      #",
    "#    ###    #",
    "#  ###      #",
    "#       #   #",
    "#############"
    ])


player = Camera(90,0,480//2,480//2,map,window,(1280,962))

while True :
    for i in pygame.event.get() :
        if i.type == pygame.QUIT :
            pygame.quit()
            exit()
    pygame.display.flip()
    pygame.draw.rect(window,pygame.Color(0,0,0),(0,0,int(1280),int(962)),0)
    player.render3D(player.scanWalls())
    TwoDRaycast.displayAll(map,player,window)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] : 
        player.Rotate(-5)
    elif keys[pygame.K_d]:
        player.Rotate(5)
    elif keys[pygame.K_z]:
        player.Move(5)
    elif keys[pygame.K_s]:
        player.Move(-5)
