import os
import pygame
import sys
from pygame.locals import *

class ParallaxLayer(pygame.sprite.Sprite):
    
    def __init__(self, y, image, movement_rate):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.movement_rate = movement_rate
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = 0
        self.width = self.rect.width
        
    def change_speed(self, x):
        self.movement_rate *= x
    
    def set_position(self, x):
        self.rect.left = x
        
    def update(self):
        self.rect.left += self.movement_rate
            
        
class ParallaxLayers():
    
    __group_list =[]
    __isPaused = False
    __isSlow = False
    __isFast = False
    
    def __init__(self, screen):
        self.__screen = screen
        self.__width = screen.get_width()
        
    def add_layer(self, layer, height, fill):
        if fill:
            extra_width = layer.width - 1
            total_tile_coverage = extra_width + self.__width
            group = pygame.sprite.Group()
            layer.set_position(0)
            group.add(layer)
            left_position = layer.width
            while left_position <= total_tile_coverage:
                new_layer = ParallaxLayer(layer.y, layer.image,
                                          layer.movement_rate)
                new_layer.set_position(left_position)
                left_position += layer.width
                group.add(new_layer)
            self.__group_list.append(group) 
        
    def decrease_speed(self):
        print ('decrease speed')
        
    def get_groups(self):
        return self.__group_list
        
    def increase_speed(self):
        print ('increase speed')
        
    def pause(self):
        print ('pause')
        
    def resume(self):
        print ('resume')
       
    def update (self):
        self.rect.left -= self.movement_rate
        