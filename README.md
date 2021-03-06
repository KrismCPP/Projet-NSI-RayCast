# Projet-NSI-Terminale - Backrooms

### Présentation du Projet / Jeu
Dans le cadre de notre Projet de NSI pour l'année de Terminale, nous avons essayé de représenter Les Backrooms.

Le concept de ce jeu est de s'échapper du labyrinthe le plus rapidement possible. Lorsque vous trouverez la sortie, le hasard décidera pour vous si vous aurez la vie saine et sauve, ou si vous devrez affronter un niveau plus difficile. Soyez rapide, au bout d'un certain temps, un monstre vous pourchassera, et vous n'y survivrait pas !

### Méthodes et Notions Utilisées
* Nous avons utilisé la bibliothèque PyGame afin de développer le Jeu.
* A travers ce projet, nous avons pu obtenir un rendu 3D d'un labyrinthe, au départ représenté en 2D. Cela a ainsi nécessité de manipuler des calculs vectorielles afin d'obtenir un rendu propre et net des distances entre le Joueur et les murs sur son champs de vision.
* La génération des Labyrinthes se base sur l'algorithme de Prim.
* La recherche du chemin le plus court entre le Monstre et le Joueur se fait grâce à un parcours en BFS.

### Nécessite
* Python
* Bibliothèques : PyGame et Matplotlib
* Sortie Audio

### Comment y Jouer
* Executer le fichier Python main.py
* Utiliser la souris sur les interfaces de Menu
* Utiliser les flèches directionnelles ZQSD ou WASD (Modifiable avec la touche TAB)

### Membres Participants
* Eliot Rabin
* Tristan Henaff
* Adrien Leschaves
* Ashwine Tirouvaroul
