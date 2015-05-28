import os
import pygame
import sys
from pygame.locals import *

class ParallaxLayer():
    
    def __init__(self, x, y, image_location, movement_rate):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.movement_rate = movement_rate
        
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, image_location)
        
        self.image = pygame.image.load(image_directory)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        
    def updated(self):
        self.rect.left -= self.movement_rate
            
    def change_speed(self, x):
        self.movement_rate *= x
        
class ParallaxLayers():
    
    def __init__(self, y, surface, tile_width, image_location, 
                          movement_speed):
        self.screen_width = surface.get_width()
        self.y = y
        self.tile_width = tile_width
        self.image_location = image_location
        self.movement_speed = movement_speed
        
    def update(self):
        ground_list = []
        for i in range(len(self.y)):
            x = 0
            while x < self.screen_width:
                layer = ParallaxLayer(x, self.y[i], self.image_location[i], 
                                      self.movement_speed[i])
                ground_list.append(layer)
                x += self.tile_width[i]
        return ground_list
        
    def change_speed(self, modifier):
        for i in len(self.movement_speed):
            self.movement_speed *= modifier    
   