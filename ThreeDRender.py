################################################################################
################################################################################
##################   Rendu 3D - Fonctions et Classes Utiles   ##################
################################################################################
################################################################################

'''IMPORTATION DES MODULES'''
from TwoDRaycast import *


'''Classe'''

class Camera (Player) :
    """ Classe Fille de Player """
    def __init__(self, fov, angle, x, y, map, window,resolution, hands : bool) -> None:
        super().__init__(fov, angle, x, y, map, window)
        self.resolution = resolution
        self.hand = Hands(resolution)
        self.handGroup = pygame.sprite.Group()
        self.handGroup.add(self.hand)
        self.hands = hands

    def GetHeight(self, distance) :
        """Renvoie selon la distance le point de l'axe y du haut et du bas du mur"""

        halfScreen = self.resolution[1]//2

        if distance == float('inf') :
            return halfScreen,halfScreen

        height = (962//30*self.resolution[1])/distance

        StartHeight = halfScreen - height//2
        EndHeight = halfScreen + height//2

        return StartHeight,EndHeight


    def GetBlackTone(self,distance) :
        """ Renvoie ue nuance de gris du mur selon la distance """
        if distance == float('inf') :
            return 0
        blacktone = floor(distance/self.mapScale * 450)
        if blacktone > 255:
            blacktone = 255
        return 255-blacktone



    def drawTexturedLine(self,point,distance,duplicateLines,texture,partOfScreen) :
        """ Dessine la ligne des textures """
        height = self.GetHeight(distance)
        if height == (self.resolution[1]//2,self.resolution[1]//2) :
            return
        lenHeight = height[1]-height[0]
        line = texture[0]
        toDark = self.GetBlackTone(distance)/255
        for i in range (len(line)) :
            startPoint = Vector2D(partOfScreen*int(duplicateLines),i/len(line)*lenHeight+height[0])
            endPoint = Vector2D(partOfScreen*int(duplicateLines),(i+1)/len(line)*lenHeight+height[0])
            pygame.draw.line(self.window,pygame.Color(int(line[i][0]*255*toDark),int(line[i][1]*255*toDark),int(line[i][2]*255*toDark)),(startPoint.x,startPoint.y),(endPoint.x,+endPoint.y),int(duplicateLines))
        #Trouve un point sur l'axe x en l'adaptant ?? la resolution


    def render3D(self, scans : list) :
        """ scans : scanWalls()
        Permet d'afficher le rendu 3D sur la fen??tre graphique
        """
        #Adapte l'affiche des murs selon la r??solution
        duplicateLines = math.ceil(1/len(scans)*self.resolution[0])
        for i in range (len(scans)) :
            self.drawTexturedLine(scans[i][1],scans[i][0],duplicateLines,Wall,i)
        if self.hands :
            self.handGroup.draw(self.window)
            self.hand.anim()

class Hands(pygame.sprite.Sprite) :
    """Classe permettant l'affiche des mains"""
    def __init__(self,resolutionEcran) -> None:
        super(Hands, self).__init__()
        self.resolutionEcran = resolutionEcran
        image = pygame.image.load("mains_animation/mains1.png")
        self.image = pygame.transform.scale(image, (self.resolutionEcran[0], self.resolutionEcran[1]))
        self.rect = self.image.get_rect()
        self.clockChange = 1
        self.currentClock = 0
        self.imageIndex = 1
    def anim(self) :
        """
        Permet d'animer les mains
        """
        if self.currentClock == self.clockChange :
            self.imageIndex += 1
            self.currentClock = 0
        if self.imageIndex > 6 :
            self.imageIndex = 1
        self.currentClock += 1
        image = pygame.image.load("mains_animation/mains"+str(self.imageIndex)+".png")
        self.image = pygame.transform.scale(image, (self.resolutionEcran[0], self.resolutionEcran[1]))
