import pygame
import random
from socket import *
import thread

#Define some colors
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)


serverName = "localhost"
serverPort = 9215
clientSocket = socket(AF_INET, SOCK_DGRAM)


class Player(pygame.sprite.Sprite):
        """ The class is the player-controlled sprite. """
 
        def __init__(self, x, y, off = 0):
                """Constructor function"""
        # Call the parent's constructor
                super(Player, self).__init__()
                self.p=off                
        # Set height, width
                if (off == False):
                        self.image = pygame.image.load("ss2.png")
                else:
                        self.image = pygame.image.load("spiral2.png")
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
                if(self.p==1):
                        self.rect.x += self.change_x
                else:
                        self.rect.x -= self.change_x
                #print "In Update"
                '''if (self.rect.y <= 30):
                        self.rect.y += self.change_y
                elif (self.rect.y <= 350):
                        self.rect.y -= self.change_y'''
                        
pygame.init()

def listener():
        while 1:
                msg = clientSocket.recvfrom(2048)
                if(msg[0][0]=='p'):
                        player1.rect.y = int(msg[0][1:])
                else:
                        bullet = int(msg[0][1:])                        
                        mov_block = Player(15+10, bullet,1)
                        moving_block.add(mov_block)



screen_width = 700
screen_height = 400


player1 = Player(15,60)
player2 = Player(670,60)
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player1)
all_sprites_list.add(player2)
ini= 'ready'
print "sending msg"
clientSocket.sendto(ini,(serverName,serverPort))
print "msg sent"
while 1:
    mesg , serverAddress = clientSocket.recvfrom(2048)
    if(mesg=='ready'):
        print mesg
        try:
                thread.start_new_thread( listener, ())
        except:
                print "error here"
          
        break



count1=0
count2=0
                
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption('PLayer 2')

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
                        if event.key == pygame.K_UP and player2.rect.y >= 60:
                                player2.rect.y -= speed
                                clientSocket.sendto('p'+str(player2.rect.y),(serverName,serverPort))
                        elif event.key == pygame.K_DOWN and player2.rect.y <= 350:
                                player2.rect.y += speed
                                clientSocket.sendto('p'+str(player2.rect.y),(serverName,serverPort))
                        elif event.key == pygame.K_SPACE:
                                clientSocket.sendto("b"+ str(player2.rect.y),(serverName,serverPort))
                                mov_block = Player(player2.rect.x-10, player2.rect.y,2)
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
                        print "player 1 loses"
                        pygame.quit()
                        
        bullet2=pygame.sprite.spritecollideany(player2,moving_block, collided = None)
        if(bullet2!=None):
                moving_block.remove(bullet2)
                count2+=1
                if(count2>5):
                        print "player 2 loses"
                        pygame.quit()
        
        clock.tick(10)
        
        
pygame.quit()
        
