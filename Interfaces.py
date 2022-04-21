################################################################################
################################################################################
###########################   Interfaces des Menus   ###########################
################################################################################
################################################################################

'''IMPORTATION DES MODULES'''
from Utils import *

'''Fonctions '''

'''Importation des polices d'écriture'''
pygame.font.init()
pixelife_font = pygame.font.Font("font/pixellife.TTF", 50) #importation de police pixellife

def menu_principal(screen):
    '''Importation et mise en place de l'image de fond du menu'''
    background = pygame.image.load('interface/backroom_img.png')
    screen.blit(background,(-100,0))

    '''Creation de texte dans le menu de lancement'''
    pygame.display.set_caption('Welcome to the backroom')
    textsurface = pixelife_font.render('Welcome to the backroom', False, (255, 255, 255))
    text_rect = textsurface.get_rect(center = (320,80)) #Permet de centrer le texte
    screen.blit(textsurface, text_rect)

    '''Creation du bouton pour lancer la partie'''
    start_bouton = pixelife_font.render('Start' , True , (255, 255, 255))
    start_text_rect = start_bouton.get_rect(center = (320,200))
    screen.blit(start_bouton, start_text_rect)

    '''Creation du bouton pour quitter le jeu'''
    quit_bouton = pixelife_font.render('Quit' , True , (255, 255, 255))
    quit_text_rect = quit_bouton.get_rect(center = (320,300))
    screen.blit(quit_bouton, quit_text_rect)

    '''Actualise l'affichage'''
    pygame.display.flip()


    running = True

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #Permet de fermer le jeu
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN: #Si le click gauche presser
                if 250 <= mouse[0] <= 400 and 180 <= mouse[1] <= 240: #Lance le jeu si le click gauche est presser dans la zone de texte start
                    return

                if 250 <= mouse[0] <= 400 and 280 <= mouse[1] <= 330: #Quitte le jeu si le click gauche est presser dans la zone de texte Quit
                    pygame.quit()
                    exit()

def menu_gameover(screen):
    '''Importation et mise en place de l'image de fond du menu'''
    background = pygame.image.load('interface/gameover.jpg')
    screen.blit(background,(0,0))

    '''Creation du texte Game Over'''
    start_bouton = pixelife_font.render('GAME OVER' , True , (255, 255, 255))
    start_text_rect = start_bouton.get_rect(center = (320,200))
    screen.blit(start_bouton, start_text_rect)

    '''Creation du bouton pour Retry lpour revenir au menu principal'''
    retry_bouton = pixelife_font.render('Retry' , True , (255, 255, 255))
    retry_text_rect = retry_bouton.get_rect(center = (320,300))
    screen.blit(retry_bouton, retry_text_rect)

    '''Actualise l'affichage'''
    pygame.display.flip()


    running = True

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #Permet de fermer le jeu
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= mouse[0] <= 400 and 280 <= mouse[1] <= 330: #Retourne au menu principal si le click gauche est presser dans la zone de texte Retry
                    menu_principal(screen)
                    return 0

def menu_arrivee(screen):
    '''Importation et mise en place de l'image de fond du menu'''
    background = pygame.image.load('interface/sortie.png')
    screen.blit(background,(0,0))

    '''Creation du texte d'arrivée'''
    arriver_text = pixelife_font.render('Vous etes sorti' , True , (255, 255, 255))
    arriver_text_rect = arriver_text.get_rect(center = (320,200))
    screen.blit(arriver_text, arriver_text_rect)

    '''Creation du bouton pour Retry lpour revenir au menu principal'''
    retry_bouton = pixelife_font.render('Menu Principal' , True , (255, 255, 255))
    retry_text_rect = retry_bouton.get_rect(center = (320,300))
    screen.blit(retry_bouton, retry_text_rect)

    '''Actualise l'affichage'''
    pygame.display.flip()


    running = True

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #Permet de fermer le jeu
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= mouse[0] <= 400 and 280 <= mouse[1] <= 330: #Retourne au menu principal si le click gauche est presser dans la zone de texte Retry
                    menu_principal(screen)
                    return 0