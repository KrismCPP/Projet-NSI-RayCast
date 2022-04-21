################################################################################
################################################################################
###########   Classe et Fonctions utiles au fonctionnement du Jeu   ############
################################################################################
################################################################################

'''IMPORTATION DES MODULES'''
import math
from math import floor
import pygame
from matplotlib import image


'''Classe /  Fonctions '''

class Vector2D :
    def __init__(self,x,y) :
        self.x = x
        self.y = y

class Hands(pygame.sprite.Sprite) :
    def __init__(self) -> None:
        super(Hands, self).__init__()
        self.image = pygame.image.load("mains_animation/mains1.png")
        self.rect = self.image.get_rect()
        self.clockChange = 1
        self.currentClock = 0
        self.imageIndex = 1
    def anim(self) :
        if self.currentClock == self.clockChange :
            self.imageIndex += 1
            self.currentClock = 0
        if self.imageIndex > 6 :
            self.imageIndex = 1
        self.currentClock += 1
        self.image = pygame.image.load("mains_animation/mains"+str(self.imageIndex)+".png")


def rotateVector(Vector,angle) :
    x1 = Vector.x
    y1 = Vector.y

    return Vector2D(round(x1*math.cos(angle) - y1*math.sin(angle),5), round(x1*math.sin(angle) + y1*math.cos(angle),5))


#Iinitialisation des textures graphiques
Wall = image.imread('texture/mur.png')
Door = image.imread('texture/porte.png')


def stringToList(map) :
    """
    Fonction de débogage
    """
    for i in range (len(map)) :
        map[i] = list(map[i])
    return map
