import os
import pygame
import sys
from pygame.locals import *

class ParallaxLayer(pygame.sprite.Sprite):
    
    def __init__(self, y, image_location, movement_rate):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.movement_rate = movement_rate
        
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, image_location)
        
        self.image = pygame.image.load(image_directory)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        
    def change_speed(self, x):
        self.movement_rate *= x
        
    def set_position(self, x):
        self.rect.left = x
        
    def update(self):
        self.rect.left += self.movement_rate
            
        
class ParallaxLayers():
    
    def __init__(self):
        
        
    def update(self):
        
        
    def change_speed(self, modifier):
       
   