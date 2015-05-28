import os
import pygame
import sys 
from Player import Player
from pygame.locals import *

def main():
    pygame.init()
    FPS = 60
    fps_clock = pygame.time.Clock()
    
    SURFACE_WIDTH = 1000
    SURFACE_HEIGHT = 700
    SURFACE = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    pygame.display.set_caption("Final Project")
    
    active_sprite_list = pygame.sprite.Group()
    
    player = Player(350, 350)
    
    active_sprite_list.add(player)
    
    j_pressed = False
    s_pressed = False
    f_pressed = False
    
    
    while True: 
        for event in pygame.event.get():    
            
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_j:
                    print ('j pressed')
                    j_pressed = True
                if event.key == K_s:
                    print ('s pressed')
#                     s_pressed = True
                if event.key == K_f:
                    print ('f pressed')
#                     f_pressed = True
                    
            if event.type == KEYUP:
                if event.key == K_j:
                    print ('j released')
                    j_pressed = False
                if event.key == K_s:
                    print ('s released')
                    s_pressed = True
                if event.key == K_f:
                    print ('f released')
                    f_pressed = True
        
        if j_pressed:
            player.jump()
        if s_pressed:
            player.slow()
            s_pressed = False
        if f_pressed: 
            player.speed_up()
            f_pressed = False
            
        
        active_sprite_list.update()
        SURFACE.fill(pygame.Color(4, 66, 13))    
        active_sprite_list.draw(SURFACE)
        fps_clock.tick(FPS)
                
        pygame.display.update()
        
if __name__ == "__main__":
    main()
        