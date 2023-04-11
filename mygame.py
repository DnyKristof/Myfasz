import math
from tkinter import scrolledtext 
from numpy import true_divide
import pygame
from sys import exit
from sympy import *

def display_time():
    time = pygame.time.get_ticks()
    return int(round(time/1000,0))

pygame.init()
width = 1280*2
height = 720*2
screen = pygame.display.set_mode((width,height))

path = "D:\Python\Games\Mygame\\"
font = pygame.font.Font("slkscr.ttf",50)

gravity = 0.1

kuty = pygame.image.load("kutymuty.png").convert_alpha()

ground = pygame.image.load("background.png").convert_alpha()
ground_rect = ground.get_rect(bottomleft =(0,height))

cica = pygame.image.load("cicmic.png").convert_alpha() ; cicax=400 ; cicay=height-cica.get_height()-ground.get_height() ; cicavx=0 ; cicavy=0; cicaa=0.03
cica_rect = cica.get_rect(topleft=(cicax,cicay)) 
isMovingright = False
isMovingleft = False

player = pygame.image.load("Player\p1_walk\PNG\p1_walk01.png").convert_alpha() ; playerx=0 ; playery = cicay ; playervx = 0 ; playervy = 0 ; playera = 0.14
player_rect = player.get_rect(bottomleft=(playerx,height-ground.get_height())) 


clock = pygame.time.Clock()

pygame.display.set_caption("Degla")
#pygame.display.set_icon(icon)

test_surface = pygame.Surface((width,height))
test_surface.fill('black')


korbe = pygame.image.load("szivi32x32.png").convert_alpha()
korbe_rect = korbe.get_rect(center=(cica_rect.x,cica_rect.y)) ; korbevx =0 ; korbevy = 0 ; korszog = 0 ; korszogsebesseg = math.pi ; periodusido = 1/144

korbe2 = pygame.image.load("szivi32x32.png").convert_alpha()
korbe2_rect = korbe2.get_rect(center=(cica_rect.x,cica_rect.y))

tolni = pygame.Surface((32,32))
tolni.fill('red')
tolni_rect = tolni.get_rect(bottomleft=(width/2,height-ground.get_height()))

korbelista=[korbe]

iframe= 0

game_active = True

sebesseg = 7
pontszerzes_sebesseg = 1

score = 0
while True:
    
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN: #keys = pygame.key.get_pressed()[pygame.K_SPACE]
            if event.key == pygame.K_SPACE and cicavy == 0:
                cicavy = -10
            if event.key == pygame.K_a:
                cicavx -= sebesseg
            if event.key == pygame.K_d:
                cicavx += sebesseg
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a :
                cicavx += sebesseg
            if event.key == pygame.K_d:
                cicavx -=sebesseg

    text = font.render(str(display_time()),False,'white')
    
    
    if game_active:
        #textúrák sorrendje
        screen.blit(test_surface,(0,0))

        screen.blit(ground,ground_rect)

        screen.blit(text,(width/2,200))

        screen.blit(cica,cica_rect)

        screen.blit(player,player_rect)


        #cica kimegy a képernyőről + pontszerzés
        if cica_rect.left>width: 
            cica_rect.right=0 
            score+=1
            korbelista.append(korbe.copy())
            if playervx >= 0:
                playervx += pontszerzes_sebesseg
            else:
                playervx-=pontszerzes_sebesseg
        if cica_rect.right < 0 : cica_rect.left = width

        

        

        
        
        #player lepattan a széléről
        if player_rect.right>width: playervx*=-1 
        if player_rect.left < 0 : playervx*=-1 

        
        #szivecskék a cica körül + pontszerzés
        for i in range(len(korbelista)):
            screen.blit(korbelista[i],korbe_rect)
            korbe_rect.x = 200*math.cos(korszog*periodusido+(math.pi/len(korbelista)*2)*i)+cica_rect.center[0]
            korbe_rect.y = 100*math.sin(korszog*periodusido+(math.pi/len(korbelista)*2)*i)+cica_rect.center[1]
            if player_rect.colliderect(korbelista[i].get_rect(center=(korbe_rect.x,korbe_rect.y))) and iframe == 0 :
                player_rect.x = 0
                score+=1
                iframe = 144/3
                if playervx >= 0:
                    playervx +=pontszerzes_sebesseg
                else:
                    playervx-=pontszerzes_sebesseg
        

        
        #helyzetek frissítése
        korszog+=korszogsebesseg
        player_rect.x+=playervx
        player_rect.y-=playervy
        cica_rect.x +=cicavx
        cica_rect.y +=cicavy
        
        

        #tolnivaló
        screen.blit(tolni,tolni_rect)
        if tolni_rect.colliderect(cica_rect) and tolni_rect.bottomleft < cica_rect.bottomright: tolni_rect.bottomleft = cica_rect.bottomright
        
        #padló a cicának + gravitáció
        if cica_rect.bottom > ground_rect.top  : cica_rect.bottom = ground_rect.top ; cicavy = 0
        elif cicavy != 0 : cicavy += 0.1

        # halál
        if cica_rect.colliderect(player_rect): game_active = True
        
        if iframe>0 : iframe-=1

    # halál képernyő
    else:
        screen.blit(test_surface,(0,0))
        if pygame.key.get_pressed()[pygame.K_k]:
            game_active = True
        player_rect.x = 0
        cica_rect.x = 500
        score = 0
        
        
    
    pygame.display.update()
    clock.tick(144)