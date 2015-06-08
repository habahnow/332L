import os
import pygame
from spritesheet_functions import SpriteSheet
import sys

debugging = False

class Ghost(pygame.sprite.Sprite):
    __gravity = 1
    __movement_frames = []
    __current_frame_reference = 0
    __movement_counter = 0
    __movement_counter_boundary = 2
    __movement_speed = 24
            
    def __init__(self, x, y):
        """
        Initializes the image at the given location.
        
        Args:
            x (int): the x coordinate to place the Sprite.
            y (int): the y coordinate to place the Sprite.
        """
        pygame.sprite.Sprite.__init__(self)

        #Get the ghost images from the Sprites folder
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, 'Sprites/ghost2.bmp')
        
        # Get the 2 images for the sprite sheet. 
        sprite_sheet = SpriteSheet(image_directory)
        image = sprite_sheet.get_image(0, 0, 62, 75)
        self.__movement_frames.append(image)
        image = sprite_sheet.get_image(64 , 0, 62, 75)
        self.__movement_frames.append(image)
        
        
        # set the Player to the first sprite
        self.image = self.__movement_frames[self.__current_frame_reference]
        
        self.rect = self.image.get_rect()
        
        # Setting the location of rectangle
        self.rect.x = x
        self.rect.y = y
        
    def set_floor(self, floor):
        self.rect.y = floor
        
        
    def slow(self):#TODO
        if debugging:
            print ('slow')
            
    def speedup(self):#TODO
        if debugging:
            print ('speedup')
            
    def update(self):#TODO
        if debugging:
            print ('update')
            
        self.__run()
       
    def __run(self):
        """
        Moves the Sprite and changes the sprite image.
        
        """
        
        if debugging:
            print ('run')
        
        if self.rect.right > 0:
            self.__movement_counter += 1
            
            if self.__movement_counter >= self.__movement_counter_boundary:
                self.__movement_counter = 0 
                self.rect.left -= self.__movement_speed
                
                # Switching the sprite image.
                self.__movement_frames.reverse()
                self.image = self.__movement_frames[0]
        
    