import os
import pygame
from spritesheet_functions import SpriteSheet
import sys

debugging = False
distance_from_floor = 20
base_movement_speed = 10

class Fast(pygame.sprite.Sprite):
    id = 0
    __gravity = 1
    __movement_counter = 0
    __movement_counter_boundary = 2
    __movement_speed = base_movement_speed + 2
            
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Get the Image icon from the Sprites folder
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, 'Sprites/fast.bmp')
        
        # Get the image for the sprite.
        
        self.image = pygame.image.load(image_directory).convert() 
        
        self.rect = self.image.get_rect()
        
        # Setting the location of rectangle
        self.rect.x = x
        self.rect.y = y
        

    def slow(self):
        if debugging:
            print ('slow')
            
    def speedup(self):
        if debugging:
            print ('speedup')
            
    def update(self):
        if debugging:
            print ('update')
            
        if self.rect.right > 0:
            self.__movement_counter += 1
            
            if self.__movement_counter >= self.__movement_counter_boundary:
                self.__movement_counter = 0 
                self.rect.left -= self.__movement_speed
        
class Slow(pygame.sprite.Sprite):
    id = 1
    __gravity = 1
    __movement_counter = 0
    __movement_counter_boundary = 2
    __movement_speed = base_movement_speed - 2
    
            
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Get the Image icon from the Sprites folder
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, 'Sprites/slow.bmp')
        
        # Get the image for the sprite.
        
        self.image = pygame.image.load(image_directory).convert() 
        
        self.rect = self.image.get_rect()
        
        # Setting the location of rectangle
        self.rect.x = x
        self.rect.y = y
        
        
    def slow(self):
        if debugging:
            print ('slow')
            
    def speedup(self):
        if debugging:
            print ('speedup')
            
    def update(self):
        if debugging:
            print ('update')
            
        if self.rect.right > 0:
            self.__movement_counter += 1
            
            if self.__movement_counter >= self.__movement_counter_boundary:
                self.__movement_counter = 0 
                self.rect.left -= self.__movement_speed
            
class UpperCut(pygame.sprite.Sprite):
    id = 2
    __gravity = 1
    __movement_counter = 0
    __movement_counter_boundary = 2
    __movement_speed = base_movement_speed
    
            
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Get the Image icon from the Sprites folder
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, 'Sprites/uppercut.bmp')
        
        # Get the image for the sprite.
        
        self.image = pygame.image.load(image_directory).convert() 
        
        self.rect = self.image.get_rect()
        
        # Setting the location of rectangle
        self.rect.x = x
        self.rect.y = y
        
    def slow(self):
        if debugging:
            print ('slow')
            
    def speedup(self):
        if debugging:
            print ('speedup')
            
    def update(self):
        if debugging:
            print ('update')
            
        if self.rect.right > 0:
            self.__movement_counter += 1
            
            if self.__movement_counter >= self.__movement_counter_boundary:
                self.__movement_counter = 0 
                self.rect.left -= self.__movement_speed
            
    
        
class Stomp(pygame.sprite.Sprite):
    id = 3
    __gravity = 1
    __movement_counter = 0
    __movement_counter_boundary = 2
    __movement_speed = base_movement_speed
    
            
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Get the Image icon from the Sprites folder
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, 'Sprites/stomp.bmp')
        
        # Get the image for the sprite.
        self.image = pygame.image.load(image_directory).convert() 
        
        self.rect = self.image.get_rect()
        
        # Setting the location of rectangle
        self.rect.x = x
        self.rect.y = y
        
        
    def slow(self):
        if debugging:
            print ('slow')
            
    def speedup(self):
        if debugging:
            print ('speedup')
            
    def update(self):
        if debugging:
            print ('update')
            
        if self.rect.right > 0:
            self.__movement_counter += 1
            
            if self.__movement_counter >= self.__movement_counter_boundary:
                self.__movement_counter = 0 
                self.rect.left -= self.__movement_speed
            
        