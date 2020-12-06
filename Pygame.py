import random
import sys
import time

import pygame
from pygame.sprite import Sprite

#Consts for sprites, game images, & music
BABY_YODA = "babyyoda.bmp"
MANDO = "mando.bmp"
KNOB = "knob.bmp"
FROG = "frog.bmp"
SHIP = "ship.bmp"
THEME_SONG = "star-wars-theme-song.wav"

#Color consts
YELLOW = (238,219,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

#Sizing consts
WIDTH = 800
HEIGHT = 600

pygame.init()

score = 0 #max score user can reach is 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baby Yoda Challenge")
clock = pygame.time.Clock()

f = pygame.font.Font("freesansbold.ttf", 30)


#----------------------------Sprite classes--------------------------------------------------------------------
class Yoda(Sprite):   
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(BABY_YODA).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (100, 100)) #scaling image to proper size (w,h)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2 - 50
        self.rect.y = HEIGHT - 100       
    def update(self):
        keys = pygame.key.get_pressed()
        dist = 5
        if keys [pygame.K_LEFT]:
            self.rect.x -= dist
        if keys [pygame.K_RIGHT]:
            self.rect.x += dist
        #Adding boundaries so sprite does not go off screen, offset by 100 to account for image size
        if self.rect.x > WIDTH - 100:
            self.rect.x = WIDTH - 100
        if self.rect.x < 0:
            self.rect.x = 0

class Ship(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(SHIP).convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 280)) #w,h
        self.rect = self.image.get_rect()
        self.rect.x = -300 #negative because I want Ship sprite to start off screen and come when music starts
        self.rect.y = HEIGHT - 200 #minus 200 to offset for HEIGHT of Ship image   
    def update(self):
        dist = 1
        self.rect.x += dist
        if self.rect.x > WIDTH:
            self.kill()

class Knob(Sprite):
    def __init__(self, y_pos):
        Sprite.__init__(self)
        self.image = pygame.image.load(KNOB).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-60) #sprite will start at random x position but minus 100 (the image size) so image does not go off screen
        self.rect.y = -9000 + y_pos #negative 9000 to start off screen so starting point to fall down is not visible, also sets how long game will go as other sprites of this class will fall in decreasing intervals
    
    def update(self):
        self.rect.y += 3
        if self.rect.y > HEIGHT:
            self.kill() #kill the sprite after it's off screen. Useful later so game will know when to end.


#------------Sprite classes that inherit from Knob class----------------------------------------------       
class Frog(Knob): 
    def __init__(self, y_pos):
        Sprite.__init__(self)
        self.image = pygame.image.load(FROG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-70)
        self.rect.y = -9000 + y_pos

class Mando(Knob):
    def __init__(self, y_pos):
        Sprite.__init__(self)
        self.image = pygame.image.load(MANDO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-100)
        self.rect.y = -9000 + y_pos


#----------------Function for starting screen-------------------------------------------------------------------
def game_intro():
    
    pygame.mixer.music.load(THEME_SONG)
    pygame.mixer.music.play(-1, 0.0) #play the song on a loop and start at the beginning 

    ship = Ship()
    sprites = pygame.sprite.RenderPlain(ship)

    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #If user presses spacebar key, game_loop function is called and the game begins     
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    game_loop()

            #Creating an easter egg inspired by Warren Robinett :P
            if event.type == pygame.MOUSEBUTTONUP:  
                pos = pygame.mouse.get_pos()
                l = pygame.font.Font("freesansbold.ttf",30)
                m = l.render("Created by Blaine Love", False, YELLOW)
                if ship.rect.collidepoint(pos):
                    pygame.mouse.set_visible(False)
                    screen.blit(m, (200,400))
                    pygame.display.update()
                    pygame.time.wait(3000) #pause the game clock for 3 seconds
                                      
        screen.fill(BLACK)

        x = pygame.font.Font("freesansbold.ttf", 40)
        y = pygame.font.Font("freesansbold.ttf",30)
        z = pygame.font.Font("freesansbold.ttf",20)
        
        a = x.render("Baby Yoda Challenge!", False, YELLOW)
        b = y.render("Press the spacebar to start", False, YELLOW)
        c = z.render("Instructions: Use the arrow keys to catch as many", False, WHITE)
        d = z.render("knobs and frogs as you can, but avoid Mando!", False, WHITE)
        e = z.render("Knob = +1", False, WHITE)
        f = z.render("Frog = +3", False, WHITE)
        g = z.render("Mando = -3", False, WHITE)

        screen.blit(a, (150,100))
        screen.blit(b, (200,150))
        screen.blit(c, (50, 220))
        screen.blit(d, (50, 250))
        screen.blit(e, (50, 300))
        screen.blit(f, (50, 330))
        screen.blit(g, (50, 360))

        sprites.update()
        sprites.update()
        sprites.draw(screen)
        pygame.display.update()


#----------------Function for ending screen----------------------------------------------------------------------
def gameover():

    screen.fill(BLACK)
    image = pygame.image.load(MANDO).convert_alpha()
    image = pygame.transform.scale(image, (500, 500))
    a = pygame.font.Font("freesansbold.ttf", 27)
    b = pygame.font.Font(None, 25)

    global score #need this since score was created in global name space 
    if score < 50:
        x = a.render("Novice Baby Yoda! Your score is " + str(score), False, YELLOW)
        y = b.render("Do or do not, there is no try! (press spacebar to play again)", False, WHITE)
    if score >=50 and score <80:
        x = a.render("Super Baby Yoda! Your score is " + str(score), False, YELLOW)
        y = b.render("One step closer to becoming a Master! (press spacebar to play again)", False, WHITE)
    if score >=80:
        x = a.render("MASTER Baby Yoda! Your score is " + str(score), False, YELLOW)
        y = b.render("Hello there.", False, WHITE)
        z = b.render("You've mastered Baby Yoda Thanks for playing! (press spacebar to play again)", False, WHITE)
        screen.blit(z, (50, 280))

    screen.blit(x, (50,200)) #x, y
    screen.blit(y, (50, 250))
    screen.blit(image, (WIDTH/2, HEIGHT/3))
    pygame.display.update()

    gameover = True

    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #If user presses spacebar key, game_loop function is called and the game starts again. Score also resets to zero.    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = 0
                    game_loop()

            pygame.display.update()
                    

#----------------Function for game logic-------------------------------------------------------------------------
def game_loop():

    pygame.mouse.set_visible(False) #hide mouse pointer so it's not in the way of the game

    yoda = Yoda()
    #Initiated lists to append sprites to
    blocks = []
    extra_blocks = []
    enemy_blocks = []

    #Appending sprites to lists. Range is how many sprites of a certain class I want in the game.
    #And changing y values so the sprites fall at decreasing intevals 
    for i in range(60):
        y = i * 150 
        blocks.append(pygame.sprite.RenderPlain(Knob(y)))
    for i in range(20):
        y = i * 350
        extra_blocks.append(pygame.sprite.RenderPlain(Frog(y)))
    for i in range(30):
        y = i * 250 
        enemy_blocks.append(pygame.sprite.RenderPlain(Mando(y)))

    sprites = pygame.sprite.RenderPlain(yoda, *blocks, *extra_blocks, *enemy_blocks)

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #incrementing or decrementing the score based on sprite collision. 
        #spritecollide detects collision and also kills the sprite (and removes from groups)       
        global score
        for i in blocks:
            score += (1*(len(pygame.sprite.spritecollide(yoda, i, True))))
        for i in extra_blocks:
            score += (3*(len(pygame.sprite.spritecollide(yoda, i, True))))
        for i in enemy_blocks:
            score -= (3*(len(pygame.sprite.spritecollide(yoda, i, True))))
            
        sprites.update()
        screen.fill(BLACK)
        t = f.render("Score = " + str(score), False, WHITE) #update the scare and blit it to the screen
        screen.blit(t, (0,0))
        sprites.update()
        sprites.draw(screen)
        pygame.display.update()

        #When there is only 1 sprite left (the yoda sprite) then the game is over and goes to the gameover screen
        if len(sprites) == 1:
            gameover()

            
#----------------------------------------------------------------------------------------------------------------

#Call game_intro function to display start screen which calls game_loop function to start the game 
game_intro()        



