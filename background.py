import os
import pygame
import sys
from pygame.locals import *

class ParallaxLayer(pygame.sprite.Sprite):
    
    def __init__(self,x, y, image, movement_rate):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.__initial_position = x
        
        self.movement_rate = movement_rate
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.width = self.rect.width
        
    def change_speed(self, x):
        self.movement_rate *= x
    
    def set_position(self, x):
        self.rect.left = x
        
    def update(self):
        next_position = self.rect.x + self.movement_rate
        if next_position <= self.__initial_position - self.rect.width:
            self.set_position(self.rect.left + self.rect.width)
        else:
            self.rect.left += self.movement_rate
       
            
        
class ParallaxLayers():
    
    __list_of_layers = []
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
            layers = []
            group.add(layer)
            left_position = layer.width
            while left_position <= total_tile_coverage:
                new_layer = ParallaxLayer(left_position, layer.y, layer.image,
                                          layer.movement_rate)
                left_position += layer.width
                group.add(new_layer)
                layers.append(new_layer)
            self.__group_list.append(group)
            self.__list_of_layers.append(layers) 
        
    def decrease_speed(self):
        print ('decrease speed')
        
    def get_groups(self):
        return self.__group_list[:]
        
    def increase_speed(self):
        print ('increase speed')
        
    def pause(self):
        print ('pause')
        
    def resume(self):
        print ('resume')
       