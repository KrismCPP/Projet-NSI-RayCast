"""Classe et Fonctions utiles au fonctionnement du Jeu"""

'''IMPORTATION DES MODULES'''
import math
from typing import Text

from matplotlib import image


'''Classe /  Fonctions '''

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

    
Wall = image.imread('mur.png')
Door = image.imread('porte.png')

print(len(Wall[3][3]))

