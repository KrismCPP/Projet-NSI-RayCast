################################################################################
################################################################################
##################   Programme Principal du Jeu - Rendu 3D   ###################
################################################################################
################################################################################

'''IMPORTATION DES MODULES'''
from ThreeDRender import *
from Laby_generator import *
from Interfaces import *
from random import randint
import time

''' Fonction exécutant le Jeu '''

def main(resolutionEcran,window,laby_genere,monster_arrival_time,nb_dep_min,niveau):
    """ EXECUTE LE JEU
    Argument :
        resolutionEcran : Resolution de la fenêtre Graphique
        window : fenêtre graphique en cours d'éxécution
        laby_genere : Labyrinthe et ses posistions d'arrivée et de départ
        monster_arrival_time : A combien de temps le monstre doit apparaitre
        nb_dep_min : Nb de déplacement min du Joueur avant celui du Monstre
    """
    global keyboard
    #______________## INITIALISATION DU NIVEAU ##______________#

    # Map Sous forme de Liste de Liste
    map,spawn,arrival = laby_genere[0],laby_genere[1],laby_genere[2]

    # Init du joueur
    player = Camera(90,90,spawn.x*48+10,spawn.y*48+10,map,window,(resolutionEcran[0],resolutionEcran[1]),True)

    # Init des configurations du Monstre
    monstre = Monster(0,(spawn.x*48 ,spawn.y*48),(spawn.y,spawn.x),map,window)
    depart = time.time() # Début du chronomètre
    nb_dep = 0 # Déplacement du Monstre en fonction du nb de dep du Joueur

    font_nb = pygame.font.Font("font/DS-DIGIT.ttf", 24)
    pixelife_font_monstre = pygame.font.Font("font/pixellife.ttf", 35)

    #______________## EXECUTION DU NIVEAU ##______________#
    sfx["lose_percentage"].play()
    while True :

        # Si l'utilisateur ferme la fenêtre
        for i in pygame.event.get() :
            if i.type == pygame.QUIT :
                pygame.quit()
                exit()

        #Permet d'actualiser la Page
        pygame.display.flip()
        pygame.draw.rect(window,pygame.Color(0,0,0),(0,0,int(resolutionEcran[0]),int(resolutionEcran[1])),0)

        #Lance le Rendu 3D
        player.render3D(player.scanWalls())

        keys = pygame.key.get_pressed()

        # Modifier la disposition des touches utilisées avec TAB
        if keys[pygame.K_TAB]:
            if keyboard == "AZERTY" : keyboard = "QWERTY"
            elif keyboard == "QWERTY" : keyboard = "AZERTY"


        # Avancer
        if keys[keyboards_rep[keyboard][0]]:
            # Si avance et tourne à gauche
            if keys[keyboards_rep[keyboard][1]] :
                player.rotate(-5)

            #Si avance et tourne à droite
            elif keys[keyboards_rep[keyboard][3]] :
                player.rotate(5)

            # Avancer
            player.move(5)
            nb_dep += 1

        # Reculer
        elif keys[keyboards_rep[keyboard][2]]:
            # Si recule et tourne à gauche
            if keys[keyboards_rep[keyboard][1]] :
                player.rotate(-10)

            #Si recule et tourne à droite
            elif keys[keyboards_rep[keyboard][3]] :
                player.rotate(10)

            # Reculer
            player.move(-5)
            nb_dep += 1


        # Tourner à gauche uniquement
        elif keys[keyboards_rep[keyboard][1]] :
            player.rotate(-10)

        # Tourner à droite uniquement
        elif keys[keyboards_rep[keyboard][3]]:
            player.rotate(10)

        ''' POUR DEBOGAGE
        # Lance le Rendu 2D si ECHAP est appuyée
        elif keys[pygame.K_ESCAPE]:
            displayAll(map,player, monstre ,window) '''

        #Affiche le pourcentage de chance de sortir en haut à droite
        exit_pourcent = 1/(niveau-3)*100
        pourcent_surface = font_nb.render('luck: ' + str(round(exit_pourcent,2)) + '%', False, (255, 255, 255))
        pourcent_rect = pourcent_surface.get_rect(center = (resolutionEcran[0]-80,15))
        window.blit(pourcent_surface, pourcent_rect)

        #Affiche le niveau en cours en bas à droite
        level_affiche = font_nb.render('Level : ' + str(niveau - 5), False, (255, 255, 255))
        level_rect = pourcent_surface.get_rect(center = (resolutionEcran[0]-40,resolutionEcran[1]-15))
        window.blit(level_affiche, level_rect)

        #Si le joueur est arrivé au pt d'arrivée
        if player.arrival((arrival.x,arrival.y)) == True :
            return randint(1,niveau-3)

        # Si le temps "inoffensif" est dépassé
        if time.time() - depart > monster_arrival_time :
            # Tous les déplacements du Joueur sup a nb_dep_min, le monstre se déplace

            #Affiche un texte qui indique que le monstre commence à se déplacer en haut à gauche
            textsurface = pixelife_font_monstre.render('The Monster is coming...!', False, (255, 255, 255))
            text_rect = textsurface.get_rect(center = (175,20))
            window.blit(textsurface, text_rect)

            if nb_dep >= nb_dep_min :

                # On cherche le chemin pour atteindre le joueur
                path = monstre.path_finding((player.pos.x,player.pos.y),(arrival.y,arrival.x) )

                if not path :
                    # Si le Monstre est déjà sur la case du Joueur
                    sfx["monster_screamer"].play()
                    while pygame.mixer.get_busy() :
                        pass
                    sfx["lost"].play()
                    return -1

                else :
                    # On déplace la position du Monstre
                    monstre.move(path[0])
                    path.pop(0)
                    sfx["monster_coming"].play()
                    if not path :
                        # Si le Monstre vient d'arriver sur la case du Joueur
                        sfx["monster_screamer"].play()
                        while pygame.mixer.get_busy() :
                            pass
                        sfx["lost"].play()
                        return -1


                # On réinitilise le nombre de déplacement du Joueur
                nb_dep = 0

'''PROGRAMME PRINCIPAL'''

if __name__ == '__main__':

    # Touches correspondantes selon le clavier pour Pygame
    keyboards_rep = {"AZERTY" : [pygame.K_z,pygame.K_q,pygame.K_s,pygame.K_d],"QWERTY" : [pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d]}
    # Disposition des touches à défaut
    keyboard = "AZERTY"

    #______________## INITIALISATION DU JEU ##______________#

    #Resolution
    resolutionEcran = [960,720]

    #Fenetre Graphique
    pygame.init()
    window = pygame.display.set_mode((resolutionEcran[0],resolutionEcran[1]))

    #Menu principal / d'accueil
    menu_principal(window,resolutionEcran)

    #______________## EXECUTION DU JEU ##______________#
    # Variable permettant de tourner le jeu en continu
    play = 0

    while play != 1 :

        # Variables permettant de tourner le jeu en continu
        play = 1
        result = 2

        #Génération du labyrinthe 0
        niveau = 5
        laby_genere = generateur_laby(niveau)
        #Initialisation de la difficulté du Niveau 0
        monster_arrival_time = 15 # en secondes
        nb_dep_min = 20

        # Tant que le Jeu n'est pas fini, lancement d'un nouveau niveau
        while result > 1 :

            # Actualisation du labytinthe
            result = main(resolutionEcran,window,laby_genere,monster_arrival_time,nb_dep_min,niveau)

            # On augmente la taille / difficulté du prochain labyrinthe
            niveau += 1
            laby_genere = generateur_laby(niveau)
            monster_arrival_time -= 0.25 # en secondes
            nb_dep_min -= 1

        if result == -1 :
            #Affiche le menu Gamover si le joueur s'est fait attrapé par le monstre
            play = menu_gameover(window,resolutionEcran)
        elif result == 1 :
            # Afficher le menu arrivée si le joueur a reussi à sortir
            play = menu_arrivee(window,resolutionEcran)


################################################################################
################################################################################
##############################  LES BACKROOMS   ################################
####################   Eliot - Tristan - Adrien - Ashwine   ####################
################################################################################
################################################################################