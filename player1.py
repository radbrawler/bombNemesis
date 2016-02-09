import pygame
import random
from socket import *
import thread

#Define some colors
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)


serverPort = 9215
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))

print("The game is started .. wating for player 2")


class Player(pygame.sprite.Sprite):
        """ The class is the player-controlled sprite. """
        
        def __init__(self, x, y, off = 0):
                """Constructor function"""
        # Call the parent's constructor
                super(Player, self).__init__()
                self.p=off;
        # Set height, width
                if (off == False):
                        self.image = pygame.image.load("ss1.png")
                else:
                        self.image = pygame.image.load("spiral1.png")
        #self.image.fill(BLACK)
        
        # Make our top-left corner the passed-in location.
                self.rect = self.image.get_rect()
                #self.rect = self.image.load(filename)
                self.rect.x = x
                self.rect.y = y
        
                self.change_x = 15
                self.change_y = 15
                
    # Find a new position for the player
        def update(self):
                ''' Change the location of the player'''
                if(self.p==1 ):
                        self.rect.x += self.change_x
                else:
                        self.rect.x -= self.change_x
                
                #print "In Update"
                '''if (self.rect.y <= 30):
                        self.rect.y += self.change_y
                elif (self.rect.y <= 350):
                        self.rect.y -= self.change_y'''
                        
pygame.init()
#this 
def listener():
        while 1:
                msg = serverSocket.recvfrom(2048)
                if( msg[0][0]=='p'):
                        player2.rect.y = int(msg[0][1:])
                else:
                        bullet = int(msg[0][1:])
                        
                        mov_block = Player(670-10, bullet,2)
                        moving_block.add(mov_block)
                     


count1=0
count2=0
screen_width = 700
screen_height = 400

player1 = Player(15,60)
player2 = Player(670,60)
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player1)
all_sprites_list.add(player2)

while 1:
        #print "here"
        mesg , clientAddress = serverSocket.recvfrom(2048)
        if(mesg):
                print( "masg recieved:  " + mesg)
                serverSocket.sendto(mesg, clientAddress)
                try:
                        thread.start_new_thread( listener, ())
                except:
                        print ("error here")  
                break






                
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('PLayer 1')

font = pygame.font.Font(None,30)

clock = pygame.time.Clock()
moving_block = pygame.sprite.Group()
speed = 10;
done = False
while not done:

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                
                elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and player1.rect.y >= 60:
                                player1.rect.y -= speed
                                serverSocket.sendto('p'+ str(player1.rect.y), clientAddress)    #this 
                        elif event.key == pygame.K_DOWN and player1.rect.y <= 350:
                                player1.rect.y += speed
                                serverSocket.sendto('p'+str(player1.rect.y), clientAddress)
                        elif event.key == pygame.K_SPACE:
                                serverSocket.sendto('b'+ str(player1.rect.y),clientAddress)     #this 
                                mov_block = Player(player1.rect.x+10, player1.rect.y,1)
                                moving_block.add(mov_block)

        screen.fill(WHITE)
        text1 = font.render(str(count1),1,(0,0,0))
        text2 = font.render(str(count2),1,(0,0,0))
        screen.blit(text1,(5,10))
        screen.blit(text2,(680,10))
        moving_block.draw(screen)
        all_sprites_list.draw(screen)
        moving_block.update()   
        pygame.display.flip()
        bullet1=pygame.sprite.spritecollideany(player1,moving_block, collided = None)
        if(bullet1!=None):
                moving_block.remove(bullet1)
                count1+=1
                if(count1>5):
                        print ("player 1 loses")
                        pygame.quit()
                        
        bullet2=pygame.sprite.spritecollideany(player2,moving_block, collided = None)
        if(bullet2!=None):
                moving_block.remove(bullet2)
                count2+=1
                if(count2>5):
                        print ("player 2 loses")
                        pygame.quit()
        


        clock.tick(10)
        
        
pygame.quit()
        
