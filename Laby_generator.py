
################################################################################
################################################################################
#########   Générateur de Labyrinthe - Fonctions et Classes Utiles   ###########
################################################################################
################################################################################

'''ALGORITHME DE PRIM'''
"""
L'algorithme de Prim comprend les étapes suivantes :

1-Commencez avec une grille pleine de cellules non visitées

2-Choisissez une case au hasard , la transformer en cellule.
Ajouter des murs autour de ce cette cellule , et met ces murs dans une liste

3-Tant qu'il y a des murs dans la liste :
    1. Choisissez un mur au hasard dans la liste. Si une seule des deux cellules
        que le mur divise est visitée, alors :
        a) Faites du mur un passage et marquez la cellule non visitée comme faisant partie du labyrinthe
        b) Ajoutez les murs voisins de la cellule à la liste des murs.
    2. Supprimer le mur de la liste
"""

'''IMPORTATION DES MODULES'''
import random
from Utils import *


'''FONCTIONS'''

######################### Fonctions importantes ################################


def cellules_voisines(mur_aléa,laby):
    """Fonction utilisé dans generateur_laby pour trouver le nombre de cellules voisines
    Renvoie ce nombre avec cellules_v """
    cellules_v = 0
    if (laby[mur_aléa[0]-1][mur_aléa[1]] == ' '):
        cellules_v += 1
    if (laby[mur_aléa[0]+1][mur_aléa[1]] == ' '):
        cellules_v += 1
    if (laby[mur_aléa[0]][mur_aléa[1]-1] == ' '):
        cellules_v +=1
    if (laby[mur_aléa[0]][mur_aléa[1]+1] == ' '):
        cellules_v += 1

    return cellules_v

#Permet de verifier les cellules
def au_dessus(laby,mur_aléa,murs_liste):
    # cellule du dessus
    if (mur_aléa[0] != 0):
        if (laby[mur_aléa[0]-1][mur_aléa[1]] != ' '):
            laby[mur_aléa[0]-1][mur_aléa[1]] = '#'
    if ([mur_aléa[0]-1, mur_aléa[1]] not in murs_liste):
        murs_liste.append([mur_aléa[0]-1, mur_aléa[1]])

def en_dessous(laby,mur_aléa,murs_liste,hauteur):
    # cellule du dessous
    if (mur_aléa[0] != hauteur-1):
        if (laby[mur_aléa[0]+1][mur_aléa[1]] != ' '):
            laby[mur_aléa[0]+1][mur_aléa[1]] = '#'
        if ([mur_aléa[0]+1, mur_aléa[1]] not in murs_liste):
            murs_liste.append([mur_aléa[0]+1, mur_aléa[1]])
def gauche(laby,mur_aléa,murs_liste):
    # cellule de gauche
    if (mur_aléa[1] != 0):
        if (laby[mur_aléa[0]][mur_aléa[1]-1] != ' '):
            laby[mur_aléa[0]][mur_aléa[1]-1] = '#'
        if ([mur_aléa[0], mur_aléa[1]-1] not in murs_liste):
            murs_liste.append([mur_aléa[0], mur_aléa[1]-1])

def droite(laby,mur_aléa,murs_liste,largeur):
    # cellule de droite
    if (mur_aléa[1] != largeur-1):
    	if (laby[mur_aléa[0]][mur_aléa[1]+1] != ' '):
    		laby[mur_aléa[0]][mur_aléa[1]+1] = '#'
    	if ([mur_aléa[0], mur_aléa[1]+1] not in murs_liste):
    		murs_liste.append([mur_aléa[0], mur_aléa[1]+1])

def sup_murs(mur,murs_liste,mur_aléa):
    # retire les murs de notre liste de murs
    for mur in murs_liste:
        if (mur[0] == mur_aléa[0] and mur[1] == mur_aléa[1]):
            murs_liste.remove(mur)



############################# Code principal ###################################

def generateur_laby(taille_laby):
    """
    Prend en argument la taille du labyrithe voulue (largeur = hauteur)
    Renvoie le labyrinthe sous la forme d'une liste de liste"""

    ###Variables d'initialisation###
    mur = 'm'
    #Espaces pleins où le joueur ne peut pas aller, représentés par un #

    cellule = ' '
    #Espaces vides où le joueur peut se deplacer, représentés par un espace

    non_visité = 'n'
    #Espaces indeterminés en nattente d'affectation

    laby= []
    #Notre Labyrinthe sera stocké dans une liste

    hauteur = taille_laby
    largeur = taille_laby
    #hauteur doit etre = à largeur pour avoir un labyrinthe carré

    laby= []
    #Notre Labyrinthe sera stocké dans une liste

    #Creer un liste avec que des cellules non visitées.
    for i in range(0, hauteur):
        ligne = []
        for j in range(0, largeur):
            ligne.append(non_visité)
        laby.append(ligne)


    #On commence par choisir le point initial de la construction du labyrinthe
    pos_depart_h = int(random.random()*hauteur)
    pos_depart_l = int(random.random()*largeur)

    #On verifie que les valeurs soient comprises dans notre "tableau"
    if (pos_depart_h == 0):
        pos_depart_h += 1
    if (pos_depart_h == hauteur-1):
    	pos_depart_h -= 1

    if (pos_depart_l == 0):
    	pos_depart_l += 1
    if (pos_depart_l == largeur-1):
    	pos_depart_l -= 1

    laby[pos_depart_h][pos_depart_l] = cellule #notre point de de départ deviens une cellule


    #On entour notre cellule de murs
    laby[pos_depart_h-1][pos_depart_l] = '#'
    laby[pos_depart_h][pos_depart_l - 1] = '#'
    laby[pos_depart_h][pos_depart_l + 1] = '#'
    laby[pos_depart_h + 1][pos_depart_l] = '#'

    #On sauvegarde ces nouveaux murs dans une liste
    murs_liste = []
    murs_liste.append([pos_depart_h - 1, pos_depart_l])
    murs_liste.append([pos_depart_h, pos_depart_l - 1])
    murs_liste.append([pos_depart_h, pos_depart_l + 1])
    murs_liste.append([pos_depart_h + 1, pos_depart_l])

############################################################################

    #Maitenant que le départ de la construction du labyrinthe est correctement
    #initialisé on commence la construction.

    while (murs_liste):
	   #On prend un mur aléatoirement dans notre liste puis on va le "verifier"
        mur_aléa = murs_liste[int(random.random()*len(murs_liste))-1]

##################################################
       	# On verifie le mur en-dessous
        if (mur_aléa[1] != 0):
            if (laby[mur_aléa[0]][mur_aléa[1]-1] == 'n' and laby[mur_aléa[0]][mur_aléa[1]+1] == ' '):

                cellules_v = cellules_voisines(mur_aléa,laby)

                if (cellules_v < 2):
                    laby[mur_aléa[0]][mur_aléa[1]] = ' '

                    en_dessous(laby,mur_aléa,murs_liste,hauteur)
                    gauche(laby,mur_aléa,murs_liste)
                    droite(laby,mur_aléa,murs_liste,largeur)

                sup_murs(mur,murs_liste,mur_aléa)
##################################################
        #  On verifie le mur au-dessus
        if (mur_aléa[0] != 0):
            if (laby[mur_aléa[0]-1][mur_aléa[1]] == 'n' and laby[mur_aléa[0]+1][mur_aléa[1]] == ' '):

                cellules_v = cellules_voisines(mur_aléa,laby)

                if (cellules_v < 2):
                    laby[mur_aléa[0]][mur_aléa[1]] = ' '

                    au_dessus(laby,mur_aléa,murs_liste)
                    gauche(laby,mur_aléa,murs_liste)
                    droite(laby,mur_aléa,murs_liste,largeur)

                sup_murs(mur,murs_liste,mur_aléa)
##################################################
        #  On verifie le mur en-dessous
        if (mur_aléa[0] != hauteur-1):
            if (laby[mur_aléa[0]+1][mur_aléa[1]] == 'n' and laby[mur_aléa[0]-1][mur_aléa[1]] == ' '):

                cellules_v = cellules_voisines(mur_aléa,laby)
                if (cellules_v < 2):

                    laby[mur_aléa[0]][mur_aléa[1]] = ' '

                    en_dessous(laby,mur_aléa,murs_liste,hauteur)
                    gauche(laby,mur_aléa,murs_liste)
                    droite(laby,mur_aléa,murs_liste,largeur)

                sup_murs(mur,murs_liste,mur_aléa)
##################################################
        # On verifie le mur a droite
       	if (mur_aléa[1] != largeur-1):
            if (laby[mur_aléa[0]][mur_aléa[1]+1] == 'n' and laby[mur_aléa[0]][mur_aléa[1]-1] == ' '):

                cellules_v = cellules_voisines(mur_aléa,laby)
                if (cellules_v < 2):

                    laby[mur_aléa[0]][mur_aléa[1]] = ' '

                    droite(laby,mur_aléa,murs_liste,largeur)
                    en_dessous(laby,mur_aléa,murs_liste,hauteur)
                    au_dessus(laby,mur_aléa,murs_liste)
                sup_murs(mur,murs_liste,mur_aléa)


        #permet de reduire notre boucle while pour qu'elle ne sois pas infini
        for mur in murs_liste:
            if (mur[0] == mur_aléa[0] and mur[1] == mur_aléa[1]):
                murs_liste.remove(mur)

    """Fin de la boucle while"""

    # remplace les cellules non-visitées par des murs
    for i in range(0, hauteur):
    	for j in range(0, largeur):
    		if (laby[i][j] == 'n'):
    			laby[i][j] = '#'

    # Fixe l'entrée
    for i in range(0, largeur):
    	if (laby[1][i] == ' '):
    		#laby[1][i] = '@'
    		pos_depart = Vector2D(i,1)
    		break
    # Fixe la sortie
    for i in range(largeur-1, 0, -1):
    	if (laby[hauteur-2][i] == ' '):
    		laby[hauteur-1][i] = ' '
    		pos_finale = Vector2D(i,hauteur-1)
    		break

    return laby,pos_depart,pos_finale


'''Affichage console du labyrinthe'''
##def Affichage(laby):
##    """FONCTION POUR DEBOGAGE"""
##    largeur = hauteur = len(laby)
##    for i in range(0, hauteur):
##        for j in range(0, largeur):
##            if (laby[i][j] == 'n'):
##                print(str(laby[i][j]), end=" ")
##            elif (laby[i][j] == ' '):
##                print(str(laby[i][j]), end=" ")
##            else:
##                print(str(laby[i][j]), end=" ")
##        print('\n')
