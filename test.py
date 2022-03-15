from graphic_mansart import *

def touche_selec():
    """ Fonction adaptée de wait_arrow() de graphic_mansart
    Attend que l'on presse une touche du clavier.
    Renvoie "up", "down", "left", "right", "escape", "enter" ou "TAB"
    suivant que l'on a tapé sur la flèche du haut, du bas, de gauche ou de droite,
    ou la touche échap, entrée ou tabulation.
    La combinaison CTRL + ALT renvoie 'hack'.
    Renvoie une chaîne vide sinon.
    Instruction bloquante.
    """
    if PYGAME_SDL_AFFICHAGE == 1 :
        affiche_all()

    pygame.event.clear()

    while 1 :
        for event in pygame.event.get() :
            if event.type == KEYDOWN:
                if event.key == K_UP :
                    return "up"
                elif event.key == K_DOWN :
                    return "down"
                elif event.key == K_LEFT :
                    return "left"
                elif event.key == K_RIGHT :
                    return "right"
                elif event.key == K_ESCAPE :
                    return "escape"
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    return "enter"
                elif event.key == K_TAB:
                    return "TAB"
                elif event.mod & pygame.KMOD_CTRL or event.mod & KMOD_ALT:
                    if event.key == K_LCTRL or event.key == K_RCTRL or event.key == K_LALT :
                        return("hack")


x=0
while x<1:
    init_graphic(750,750,bg_color=pygame.Color(206,206,206),fullscreen=0)

    for i in range(50):
        draw_pixel(i,150,pygame.Color(0,0,0))



                #Récupère la touche sélectionnée
