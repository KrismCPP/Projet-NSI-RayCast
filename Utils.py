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

def rotateVector(Vector,angle) :
    x1 = Vector.x
    y1 = Vector.y

    return Vector2D(round(x1*math.cos(angle) - y1*math.sin(angle),5), round(x1*math.sin(angle) + y1*math.cos(angle),5))


#Iinitialisation des textures graphiques
Wall = image.imread('texture/mur.png')

#Iinitialisation des sons du jeux
pygame.mixer.init()
sfx = {"lose_percentage" : pygame.mixer.Sound("sfx/lose_percentage.wav"), "lost" : pygame.mixer.Sound("sfx/lost.wav"), "menu_music" : pygame.mixer.Sound("sfx/menu_music.wav"), "mise" : pygame.mixer.Sound("sfx/mise.wav"), "monster_coming" : pygame.mixer.Sound("sfx/monster_coming.wav"), "monster_screamer" : pygame.mixer.Sound("sfx/monster_screamer.wav"), "monster_tp" : pygame.mixer.Sound("sfx/monster_tp.wav"), "move" : pygame.mixer.Sound("sfx/move.wav"),"select" : pygame.mixer.Sound("sfx/select.wav")}
StepsChannel = pygame.mixer.Channel(1)


def stringToList(map) :
    """
    Fonction de débogage
    """
    for i in range (len(map)) :
        map[i] = list(map[i])
    return map