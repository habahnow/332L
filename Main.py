import os
import pygame
import sys 
from background import ParallaxLayer
from background import ParallaxLayers
from Player import Player
from pygame.locals import *

def generate_background(width, height):
    """
    Method that generates the background
    
    Args:
        width: is the width of the screen.
        
    This method is hard coded to generate the background/platforms that the 
        Player is running on. It uses specific images in specific locations as 
        well as setting the location of the platforms and the initial speed.
    """
    movement_speed1 = -5
    movement_speed2 = -3
    movement_speed3 = -1
    
    script_dir = sys.path[0]
    image_location = 'Sprites/ground3.bmp'
    image_directory = os.path.join(script_dir, image_location)
        
    image = pygame.image.load(image_directory)
    y = height - image.get_height()
    seperation = 200 # Vertical distance between platforms.
    
    y2 = y - seperation
    y3 = y2 - seperation
    
    
    layer1 = ParallaxLayer(0, y, image, movement_speed1)
    layer2 = ParallaxLayer(0, y2, image, movement_speed2)
    layer3 = ParallaxLayer(0, y3, image, movement_speed3)
    
    layers = ParallaxLayers(width)
    fill_horizontally = True
    
    layers.add_layer(layer1, fill_horizontally)
    layers.add_layer(layer2, fill_horizontally)
    layers.add_layer(layer3, fill_horizontally)
    
    # Change the y location to be top of the image.rect so that the 
    # Player.__floor_boundaries can be changed automatically if they are 
    # changed in this method.
    y -= image.get_height()
    y2 -= image.get_height()
    y3 -= image.get_height()
    
    return (layers, [y, y2, y3])

def main():
    pygame.init()
    FPS = 60
    fps_clock = pygame.time.Clock()
    
    SURFACE_WIDTH = 1000
    SURFACE_HEIGHT = 650
    SURFACE = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    pygame.display.set_caption("Final Project")
    
     # Creating the ground layers.
    (layers, floor_locations) = generate_background(SURFACE_WIDTH, 
                                                    SURFACE_HEIGHT)
    
    background_groups = layers.get_groups()
    
    # Creating the player
    active_sprite_list = pygame.sprite.Group()
    player = Player(0, 490, floor_locations)
    
    active_sprite_list.add(player)
    
    j_pressed = False
    s_pressed = False
    f_pressed = False
    space_bar_pressed = False
    
   
    
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
                if event.key == K_f:
                    print ('f pressed')
                    f_pressed = True
                if event.key == K_SPACE:
                    space_bar_pressed = True
                    
            if event.type == KEYUP:
                if event.key == K_j:
                    print ('j released')
                    j_pressed = False
                if event.key == K_s:
                    print ('s released')
                    s_pressed = True
                if event.key == K_f:
                    print ('f released')
                    f_pressed = False
                if event.key == K_SPACE:
                    space_bar_pressed = False
        
        if space_bar_pressed:
            player.jump()
        if s_pressed:
            s_pressed = False
        if f_pressed:
            player.drop_down()
            
        
        SURFACE.fill(pygame.Color(4, 66, 13))
        
        # Updates and draws the background
        for group in background_groups:
            group.update()
            group.draw(SURFACE)
        
        active_sprite_list.update()    
        active_sprite_list.draw(SURFACE)
        
            
        fps_clock.tick(FPS)
    
                
        pygame.display.update()
        
if __name__ == "__main__":
    main()
        