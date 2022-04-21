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
    #______________## INITIALISATION DU NIVEAU ##______________#

    # Map Sous forme de Liste de Liste
    map,spawn,arrival = laby_genere[0],laby_genere[1],laby_genere[2]

    # Init du joueur
    player = Camera(90,90,spawn.x*48+10,spawn.y*48+10,map,window,(resolutionEcran[0],resolutionEcran[1]))

    # Init des configurations du Monstre
    monstre = Monster(0,(spawn.x*48 ,spawn.y*48),(spawn.y,spawn.x),map,window)
    depart = time.time() # Début du chronomètre
    nb_dep = 0 # Déplacement du Monstre en fonction du nb de dep du Joueur


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


        ''' TOUCHES ORDINAIRES '''
        """
        # Tourne à gauche
        if keys[pygame.K_q] :
            player.rotate(-10)

        # Tourne à droite
        elif keys[pygame.K_d]:
            player.rotate(10)

        # Avance
        elif keys[pygame.K_z]:
            player.move(5)
            nb_dep += 1

        # Recule
        elif keys[pygame.K_s]:
            player.move(-5)
            nb_dep += 1
        # Lance le Rendu 2D si TAB est appuyée
        elif keys[pygame.K_TAB]:
            displayAll(map,player,monstre,window)
        """


        ''' TOUCHES SOUS PYGAME'''

        # Tourne à gauche
        if keys[pygame.K_a] :
            player.rotate(-10)

        # Tourne à droite
        elif keys[pygame.K_d]:
            player.rotate(10)

        # Avance
        elif keys[pygame.K_w]:
            player.move(5)
            nb_dep += 1

        # Recule
        elif keys[pygame.K_s]:
            player.move(-5)
            nb_dep += 1
        # Lance le Rendu 2D si TAB est appuyée
        elif keys[pygame.K_TAB]:
            displayAll(map,player, monstre ,window)



        #Si le joueur est arrivé au pt d'arrivée
        if player.arrival((arrival.x,arrival.y)) == True :
            return randint(1,niveau)

        # Si le temps "inoffensif" est dépassé
        if time.time() - depart > monster_arrival_time :
            # Tous les déplacements du Joueur sup a nb_dep_min, le monstre se déplace
            if nb_dep >= nb_dep_min :

                # On cherche le chemin pour atteindre le joueur
                path = monstre.path_finding((player.pos.x,player.pos.y),(arrival.y,arrival.x) )

                if not path :
                    # Si le Monstre est déjà sur la case du Joueur
                    sfx["monster_screamer"].play()
                    while pygame.mixer.get_busy() :
                        pass
                    sfx["lost"].play()
                    #menu_gameover(window)
                    return -1

                else :
                    # On déplace la position du Monstre
                    monstre.move(path[0])
                    path.pop(0)
                    if not path :
                        # Si le Monstre vient d'arriver sur la case du Joueur
                        sfx["monster_screamer"].play()
                        while pygame.mixer.get_busy() :
                            pass
                        sfx["lost"].play()
                        #menu_gameover(window)
                        return -1


                # On réinitilise le nombre de déplacement du Joueur
                nb_dep = 0

'''PROGRAMME PRINCIPAL'''

if __name__ == '__main__':

    #______________## INITIALISATION DU JEU ##______________#

    #Resolution
    resolutionEcran = [640,480]

    #Fenetre Graphique
    pygame.init()
    window = pygame.display.set_mode((resolutionEcran[0],resolutionEcran[1]))

    #Menu principal / d'accueil
    menu_principal(window)

    #______________## EXECUTION DU JEU ##______________#
    # Variable permettant de tourner le jeu en continu
    play = 0

    while play != 1 :

        # Variables permettant de tourner le jeu en continu
        play = 1
        result = 2

        #Génération du labyrinthe 0
        niveau = 3
        laby_genere = generateur_laby(niveau)
        #Initialisation de la difficulté du Niveau 0
        monster_arrival_time = 10 # en secondes
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
            play = menu_gameover(window)
        elif result == 1 :
            # Afficher le menu arrivée si le joueur a reussi à sortir
            play = menu_arrivee(window)


################################################################################
################################################################################
##############################  LES BACKROOMS   ################################
####################   Eliot - Tristan - Adrien - Ashwine   ####################
################################################################################
################################################################################