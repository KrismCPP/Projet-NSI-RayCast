from cProfile import run
from cmath import pi, sqrt
from math import cos, sin
import pygame
import random

class Vector2D:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    def addVector(self, Vector) :
        self.x = Vector.x
        self.y = Vector.y

class Wall :
    def __init__(self,Point1,Point2,color) -> None:
        self.Point1 = Point1
        self.Point2 = Point2
        self.color = color

class MapCreator :
    def __init__(self, scale = None, type = None) -> None:
        self.taille = scale
        self.type = type
    def createMap(self) :
        mapTab = []
        for i in range (self.scale) :
            mapTab += [[]]
            for _ in range (self.scale) :
                mapTab[i] += [0]
        self.mapTab = mapTab
    def createMapFromTab(self, tab) :
        self.mapTab = tab
        self.scale = len(tab)
    def getMap(self) :
        return self.mapTab

class RealMap :
    def __init__(self, MapCreator,scale) -> None:
        self.scale = scale
        self.MapCreator = MapCreator
        self.walls = []

        for i in range (MapCreator.scale) :
            for j in range (MapCreator.scale) :
                if MapCreator[i][j] == 1 :
                    x1 = j/MapCreator.scale * scale
                    y1 = i/MapCreator.scale * scale

                    x2 = j/MapCreator.scale * scale + 1/MapCreator.scale 
                    y2 = i/MapCreator.scale * scale

                    x3 = j/MapCreator.scale * scale 
                    y3 = i/MapCreator.scale * scale + 1/MapCreator.scale 

                    x4 = j/MapCreator.scale * scale + 1/MapCreator.scale 
                    y4 = i/MapCreator.scale * scale + 1/MapCreator.scale 

                    self.walls += [Wall(Vector2D(x1,y1),Vector2D(x2,y2))]
                    self.walls += [Wall(Vector2D(x1,y1),Vector2D(x3,y3))]
                    self.walls += [Wall(Vector2D(x4,y4),Vector2D(x2,y2))]
                    self.walls += [Wall(Vector2D(x4,y4),Vector2D(x3,y3))]

class Game :
    def __init__(self,x,y,RealMap) -> None:
        self.resolution = (x,y)
        self.RealMap = RealMap

class POV :
    def __init__(self, FOV, Game) -> None:
        self.position = Vector2D(0,0)
        self.camAngle = 0
        self.FOV = FOV
        self.Game = Game

    def moveCam(self, move) :
        self.camAngle += move
    
    def movePosition(self, Vector2D) :
        self.position.addVector(Vector2D)

    def getCamAngle(self) :
        return self.camAngle
    
    def getPosition(self) :
        return self.position
    
    def scanWall(self) :
        scans = []
        mainRay = Ray2D(Vector2D(1,0),self)
        mainRay.rotateRay(self.camAngle*(pi/180))
        for i in range ((-self.FOV*self.Game.resolution[0]//2)//2,(self.FOV*self.Game.resolution[0]//2)//2):
            a = (i/self.Game.resolution[0]) * (self.FOV/self.Game.resolution[0]) 
            VectorForNewRay = mainRay.ParmEquation[1]
            Ray = Ray2D(VectorForNewRay,self)
            Ray2D.rotateRay(a*(pi/180))
            scans += [Ray2D.intersection(Game.RealMap)[1]]
        return scans

        
class Ray2D :
    def __init__(self,Vector2D,pov) -> None:
        self.ParmEquation = (pov.position,Vector2D)

    def intersection(self, RealMap) :
        intersections = []
        for i in RealMap.walls :
            d = (i.point1.x - i.point2.x) * (self.ParmEquation[0].y - self.ParmEquation[1].y) - (i.point1.y - i.point2.y) * (self.ParmEquation[0].x - self.ParmEquation[1].x)
            if d == 0 :
                continue
            else : 
                t = ((i.point1.x - self.ParmEquation[0].x) * (self.ParmEquation[0].y - self.ParmEquation[1].y) - (i.point1.y - self.ParmEquation[0].y) * (self.ParmEquation[0].x - self.ParmEquation[1].x)) / d
                u = ((i.point1.x - i.point2.x) * (i.point1.y - self.ParmEquation[0].y) - (i.point1.y - self.ParmEquation[0].y) * (i.point1.x - self.ParmEquation[0].x)) / d
                if t > 0 and t < 1 and u > 0 : 
                    a1 = ((i.point2.y - i.point1.y) /  (i.point2.x - i.point1.x))
                    b1 = i.point2.y -(a1*i.point2.x)
                    
                    a2 = ((self.ParmEquation[1].y - self.ParmEquation[0].y) /  (self.ParmEquation[1].x - self.ParmEquation[0].x))
                    b2 = self.ParmEquation[1].y -(a2*self.ParmEquation[1].x)

                    x = (b2-b1)/(a1-a2)
                    y =  a1*x - b1

                    intersections += [Vector2D(x,y)]
        
                    shortestDistance = intersections[0]
                    for l in intersections :
                        shortest = sqrt((self.ParmEquation[0].x - shortestDistance.x)**2 + (self.ParmEquation[0].y - shortestDistance.y)**2)
                        next = sqrt((self.ParmEquation[0].x - l.x)**2 + (self.ParmEquation[0].y - l.y)**2)
                        if next <= shortest :
                            shortestDistance = l
                        return shortestDistance,shortest
        return Vector2D(0,0),-1
    
    

    def rotateRay(self, angle) :
        x = self.ParmEquation[1].x
        y = self.ParmEquation[1].y

        self.ParmEquation[1].x = round(x*cos(angle) - y*sin(angle),2)
        self.ParmEquation[1].y = round(x*sin(angle) + y*cos(angle),2)
