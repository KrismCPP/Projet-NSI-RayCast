from dis import dis
from hashlib import new

from sympy import factor, false, true
from Utils import *
from graphic_mansart import *
import pygame


pygame.init()

class Player :
    def __init__(self,fov,angle,x,y,map) -> None:
        self.fov = fov
        self.angle = angle
        self.pos = Vector2D(x,y)
        self.dir = rotateVector(Vector2D(1,0),angle*math.pi/180)
        self.map = map
    
    def Move(self,speed) :
        self.pos.x += self.dir.x * speed
        self.pos.y += self.dir.y * speed

    def Rotate(self, angle) :
        self.angle += angle
        self.dir = rotateVector(Vector2D(1,0),self.angle*math.pi/180)
    
    def drawRay(self, Vector) :
        pygame.draw.line(window,pygame.Color(0,0,255),(self.pos.x, self.pos.y),(Vector.x,Vector.y),1)

    def drawAllRays(self) :
        for i in range(-self.fov//2, self.fov//2) :
            
            angle = i * math.pi/180

            newVector = rotateVector(self.dir,angle)

            posx = self.pos.x 
            posy = self.pos.y 

            i = 0

            distancex = 0
            distancey = 0

            x1 = 0
            y1 = 0

            x2 = 0
            y2 = 0

            
            cadrex = floor(posx/ 480 * len(self.map))
            cadrey = floor(posy/ 480 * len(self.map))

            while self.map[cadrey][cadrex] != "#" :

                i += 1
                
                facteurx = floor(posx+i)-posx

                x1 = newVector.x*facteurx+posx
                y1 = newVector.y*facteurx+posy

                cadrex = floor(x1/ 480 * len(self.map))
                cadrey = floor(y1/ 480 * len(self.map))

                if self.map[cadrey][cadrex] == "#" :

                    distancex = math.sqrt((posx - x1)**2 + (posy - y1)**2)

            

            i = 0

            cadrex = floor(posx/ 480 * len(self.map))
            cadrey = floor(posy/ 480 * len(self.map))

            while self.map[cadrey][cadrex] != "#" :
                i += 1
                
                facteurx = floor(posx+i)-posx

                x2 = newVector.x*facteurx+posx
                y2 = newVector.y*facteurx+posy

                cadrex = floor(x2/ 480 * len(self.map))
                cadrey = floor(y2/ 480 * len(self.map))
                if self.map[cadrey][cadrex] == "#" :

                    distancey = math.sqrt((posx - x2)**2 + (posy - y2)**2)
                

            if distancex > distancey :
                self.drawRay(Vector2D(x2,y2))
            else : 
                self.drawRay(Vector2D(x1,y1))
            


    


    
map = stringToList([
    "##########",
    "#   # #  #",
    "#  ##    #",
    "#   #    #",
    "#        #",
    "#        #",
    "#    ##  #",
    "#     #  #",
    "#     #  #",
    "##########"
    ])


window = pygame.display.set_mode((480,480))

def displayAll(map,player) :
    for i in range (len(map)) :
        for j in range (len(map[i])) :
            if map[i][j] == "#" :
                pygame.draw.rect(window,pygame.Color(0,0,0),(480/10*j,480/10*i,int(480/10),int(480/10)))
            else :
                pygame.draw.rect(window,pygame.Color(255,255,255),(480/10*j,480/10*i,int(480/10),int(480/10)))
    pygame.draw.circle(window,pygame.Color(255,0,0),(int(player.pos.x),int(player.pos.y)),5)
    player.drawAllRays()
player = Player(90,0,480//2,480//2,map)
while True :
    for i in pygame.event.get() :
        if i.type == pygame.QUIT :
            pygame.quit()
            exit()
    pygame.display.flip()
    displayAll(map,player)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] : 
        player.Rotate(-1)
    elif keys[pygame.K_RIGHT]:
        player.Rotate(1)
    elif keys[pygame.K_UP]:
        player.Move(1)
    elif keys[pygame.K_DOWN]:
        player.Move(-1)

