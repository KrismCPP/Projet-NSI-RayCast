################################################################################
################################################################################
###########################   Interfaces des Menus   ###########################
################################################################################
################################################################################

'''IMPORTATION DES MODULES'''
from turtle import st
from Utils import *
from ThreeDRender import * 
from Laby_generator import *

'''Fonctions '''

'''Importation des polices d'écriture'''
pygame.font.init()
pixelife_font = pygame.font.Font("font/pixellife.TTF", 50) #importation de police pixellife

def menu_principal(screen,resolutionEcran):
    """ Affiche l'interface du Menu Principal"""
    '''Importation et mise en place de l'image de fond du menu'''
    
    BackGroundLaby = generateur_laby(12)
    startPosX,startPosY = (len(BackGroundLaby[0])-1)//2,(len(BackGroundLaby[0])-1)//2
    
    index = 0
    nbOfSearch = 1
    while BackGroundLaby[0][startPosY][startPosX] == "#" :
        if nbOfSearch >= len(BackGroundLaby) :
            startPosX = BackGroundLaby[1].x
            startPosY = BackGroundLaby[1].y
        if index >= 4 :
            index = 0
            nbOfSearch += 1
        if index == 0 :
            startPosX += nbOfSearch
            if BackGroundLaby[0][startPosY][startPosX] == "#" :
                startPosX -= nbOfSearch
        elif index == 1 :
            startPosY += nbOfSearch
            if BackGroundLaby[0][startPosY][startPosX] == "#" :
                startPosY -= nbOfSearch
        elif index == 3 :
            startPosX -= nbOfSearch
            if BackGroundLaby[0][startPosY][startPosX] == "#" :
                startPosX += nbOfSearch
        elif index == 4 :
            startPosY -= nbOfSearch
            if BackGroundLaby[0][startPosY][startPosX] == "#" :
                startPosY += nbOfSearch
        index += 1
        
    
    BackGroudCamera = Camera(90,0,startPosX*48,startPosY*48,BackGroundLaby[0],screen,(resolutionEcran[0],resolutionEcran[1]), False)

    pygame.draw.rect(screen,pygame.Color(0,0,0),(0,0,int(resolutionEcran[0]),int(resolutionEcran[1])),0)
    BackGroudCamera.render3D(BackGroudCamera.scanWalls())

    '''Creation de texte dans le menu de lancement'''
    pygame.display.set_caption('backroom')
    def texte() :
        textsurface = pixelife_font.render('Welcome to the backroom', False, (255, 255, 255))
        text_rect = textsurface.get_rect(center = (resolutionEcran[0]//2,resolutionEcran[0]//2 - resolutionEcran[0]//3)) #Permet de centrer le texte
        screen.blit(textsurface, text_rect)

        '''Creation du bouton pour lancer la partie'''
        start_bouton = pixelife_font.render('Start' , True , (255, 255, 255))
        start_text_rect = start_bouton.get_rect(center = (resolutionEcran[0]//2,(resolutionEcran[0]//5)*2))
        screen.blit(start_bouton, start_text_rect)

        '''Creation du bouton pour quitter le jeu'''
        quit_bouton = pixelife_font.render('Quit' , True , (255, 255, 255))
        quit_text_rect = quit_bouton.get_rect(center = (resolutionEcran[0]//2,(resolutionEcran[0]//5) *3))
        screen.blit(quit_bouton, quit_text_rect)

    '''Actualise l'affichage'''
    pygame.display.flip()


    while True :
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(screen,pygame.Color(0,0,0),(0,0,int(resolutionEcran[0]),int(resolutionEcran[1])),0)
        BackGroudCamera.rotate(0.5)
        BackGroudCamera.render3D(BackGroudCamera.scanWalls())
        texte()
        pygame.display.flip()
        for event in pygame.event.get():

            if event.type == pygame.QUIT: #Permet de fermer le jeu
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: #Si le click gauche presser
                if (resolutionEcran[0]//2 - 80) <= mouse[0] <= (resolutionEcran[0]//2 + 80) and ((resolutionEcran[0]//5)*2-20) <= mouse[1] <= ((resolutionEcran[0]//5)*2+20): #Lance le jeu si le click gauche est presser dans la zone de texte start
                    return

                if (resolutionEcran[0]//2 - 80) <= mouse[0] <= (resolutionEcran[0]//2 + 80) and ((resolutionEcran[0]//5)*3-20) <= mouse[1] <= ((resolutionEcran[0]//5)*3+20): #Quitte le jeu si le click gauche est presser dans la zone de texte Quit
                    pygame.quit()
                    exit()

def menu_gameover(screen,resolutionEcran):
    """ Affiche l'interface GAMEOVER"""
    '''Importation et mise en place de l'image de fond du menu'''
    background = pygame.image.load('interface/gameover.jpg')
    background = pygame.transform.scale(background, (resolutionEcran[0], resolutionEcran[1]))
    screen.blit(background,(0,0))

    '''Creation du texte Game Over'''
    start_bouton = pixelife_font.render('GAME OVER' , True , (255, 255, 255))
    start_text_rect = start_bouton.get_rect(center = (resolutionEcran[0]//2,resolutionEcran[0]//2 - resolutionEcran[0]//3))
    screen.blit(start_bouton, start_text_rect)

    '''Creation du bouton pour Retry lpour revenir au menu principal'''
    retry_bouton = pixelife_font.render('Retry' , True , (255, 255, 255))
    retry_text_rect = retry_bouton.get_rect(center = (resolutionEcran[0]//2,(resolutionEcran[0]//5) *3))
    screen.blit(retry_bouton, retry_text_rect)

    '''Actualise l'affichage'''
    pygame.display.flip()


    while True :
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #Permet de fermer le jeu
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (resolutionEcran[0]//2 - 80) <= mouse[0] <= (resolutionEcran[0]//2 + 80) and ((resolutionEcran[0]//5)*3-20) <= mouse[1] <= ((resolutionEcran[0]//5)*3+20): #Retourne au menu principal si le click gauche est presser dans la zone de texte Retry
                    menu_principal(screen,resolutionEcran)
                    return 0

def menu_arrivee(screen,resolutionEcran):

    '''Creation du texte d'arrivée'''
    arriver_text = pixelife_font.render('Vous etes sorti' , True , (255, 255, 255))
    arriver_text_rect = arriver_text.get_rect(center =(resolutionEcran[0]//2,resolutionEcran[0]//2 - resolutionEcran[0]//3))
    screen.blit(arriver_text, arriver_text_rect)

    '''Creation du bouton pour Retry lpour revenir au menu principal'''
    retry_bouton = pixelife_font.render('Menu Principal' , True , (255, 255, 255))
    retry_text_rect = retry_bouton.get_rect(center = (resolutionEcran[0]//2,(resolutionEcran[0]//5) *3))
    screen.blit(retry_bouton, retry_text_rect)

    '''Actualise l'affichage'''
    pygame.display.flip()


    while True :
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #Permet de fermer le jeu
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (resolutionEcran[0]//2 - 80) <= mouse[0] <= (resolutionEcran[0]//2 + 80) and ((resolutionEcran[0]//5)*3-20) <= mouse[1] <= ((resolutionEcran[0]//5)*3+20): #Retourne au menu principal si le click gauche est presser dans la zone de texte Retry
                    menu_principal(screen,resolutionEcran)
                    return 0
