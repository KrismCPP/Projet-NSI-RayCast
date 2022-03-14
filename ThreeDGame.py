from turtle import color

import pygame
import TwoDRaycast
import graphic_mansart

class Init :
    def __init__(self,x,y,map,fov,health) -> None:
        
        self.player = Player((x,y),health,fov,map)

class Color :
    def __init__(self, r,g,b) -> None:
        self.color = (r,g,b)

class Player :
    def __init__(self,resolution,health,FOV,map) -> None:
        self.game = TwoDRaycast.Game(resolution[0], resolution[1],map)
        self.health = health
        self.pov = TwoDRaycast.POV(FOV,self.game)
    def getHeightColors(self,dist) :
        h = self.game.resolution[1]
        LineStart = int(((dist//2)/self.game.RealMap.scale)*h)
        LineEnd = int(h-((dist//2)/self.game.RealMap.scale)*h)
        if LineStart < 0 :
            LineStart = 0
        if LineEnd >= h :
            LineEnd = h-1
        
        if dist < 0 :
            return ((0,0),Color(255,255,255))
        else :
            BlackTone = int(dist/self.game.RealMap.scale * 255)
            print((LineStart,LineEnd),BlackTone)
        return (LineStart,LineEnd),Color(BlackTone,BlackTone,BlackTone)
    def display_update(self) :
        scans = self.pov.scanWalls()
        
        for i in range (len(scans)):
            HandC = self.getHeightColors(scans[i])
            print(scans[i])
            for j in range(HandC[0][0],HandC[0][1]) :
                graphic_mansart.draw_pixel(i,j, graphic_mansart.pygame.Color(HandC[1].color[0],HandC[1].color[1],HandC[1].color[2]))
                
        print("surface")    
        
    






def CreateMap(tab,scale) :
    Map = TwoDRaycast.MapCreator()
    Map.createMapFromTab(tab)
    return TwoDRaycast.RealMap(Map,scale)

