"""
ParallaxLayer class
    
Holds the data for an image that will move in the same direction.
    
Uses whichever image is passed. The movement speed can be changed with 
    methods.
    
"""

import os
import pygame
import sys
from pygame.locals import *

class ParallaxLayer(pygame.sprite.Sprite):
   
    
    def __init__(self,x, y, image, movement_rate):
        """
        Initializes the ParallaxLayer at the given location; x, y.
        
        Args:
            x: the x location of where the image will first appear. Better if it
                is an int.
            y: the y location of where the image will first appear. Better if it
                is an int.
            image: a pygame.Surface, created from the pygame.image.load() 
                function, which will represent the layer.
            movement_rate: rate at which the image will move across the screen.
        """
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
        """
        Moves the image across a section of the screen and resets its position.
        
        The image's left side repeatedly moves from initial_position, which is 
            also x, to initial_position - (this-image's-width - 1). Uses the 
            set_position method if it reaches its boundary. 
        """
        next_position = self.rect.x + self.movement_rate
        if next_position <= self.__initial_position - self.rect.width:
            self.set_position(self.rect.left + self.rect.width)
        else:
            self.rect.left += self.movement_rate
       
       
"""
The ParallaxLayers class

This class can hold multiple ParallaxLayer(s) and, if fill is set to true, this
    class will make copies of the passed ParallaxLayer to fill the screen 
    horizontally. This class is essentially a more complicated List that is 
    focused on holding ParallaxLayer objects.
"""
        
class ParallaxLayers():
    
    __list_of_layers = []
    __group_list =[]
    __isPaused = False
    __isSlow = False
    __isFast = False
    
    def __init__(self, width):
        self.__width = width
        
    def add_layer(self, layer, fill):
        """
        Adds a ParallaxLayer to this ParallaxLayers object. 
        
        Args:
            layer: ParallaxLayer to add to this object.
            fill: if True, then this method will fill the screen horizontally 
                with layer.
                
        Adds the ParallaxLayer and, if fill is True, will fill the screen 
            horizontally with layer ensuring that there is no overlap and that
            the layers are saved in both a group and a list.
        """
        
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
       