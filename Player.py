"""
Player character class

Contains everything related to the player class.

This class displays the sprite sheet mario_edited.png that is in the Sprites
directory.

This class also controls the run animation for the sprite.



"""

import os
import pygame
from spritesheet_functions import SpriteSheet
import sys

class Player(pygame.sprite.Sprite):
    __highest = []
    __current_frame_reference = 2
    __current_frame = 0
    __gravity = 1
    __height_change = 0
    __is_jumping = False
    __jump_height = -20
    __jump_speed_modifier = 1
    __movement_frames = []#contains the images for the sprite
    __power_ups = []    
    __run_speed = 8
    __run_speed_modifier = 1
    
    
    def __init__(self, x, y):
        """
        Initializes the player class using a passes x and y coordinate
        
        Args:
            x (int): the horizontal location of where the sprite will appear.
            y (int): the vertical location of where the sprite will appear.
            
        Note:
            This init function is very reliant on the image mario_edited.png 
                being saved in a directory name Sprites.
                
            This function is also relies on a specific the specific sprite 
                sheet mario_edited.png in order to display the correct sprite.
        """
        pygame.sprite.Sprite.__init__(self)
        
        #get the player images from the Sprites folder
        script_dir = sys.path[0]
        image_directory = os.path.join(script_dir, 'Sprites/mario_edited.bmp')
        
        # get the four images for the sprite sheet. the first 3 images are 
        # walking animations while the last is the jumping sprite
        sprite_sheet = SpriteSheet(image_directory)
        image = sprite_sheet.get_image(0, 0, 50, 81)
        self.__movement_frames.append(image)
        image = sprite_sheet.get_image(50, 0, 50, 81)
        self.__movement_frames.append(image)
        image = sprite_sheet.get_image(107, 0, 50, 81)
        self.__movement_frames.append(image)
        image = sprite_sheet.get_image(162  , 0, 50, 81)
        self.__movement_frames.append(image)
        
        # set the Player to the first sprite
        self.image = self.__movement_frames[self.__current_frame_reference]
        
        self.rect = self.image.get_rect()
        
        #setting the location of rectangle
        self.rect.x = x
        self.rect.y = y
    
   
    def jump(self):
        """
        Moves the character's y locations, making it look like it's jumping.
        
        Method checks if the player is jumping with the is_jumping variable. If
            player is not, then the image is changed to the jumping image and 
            the height_change variable is set.
        """
        print ('jump')
        if not self.__is_jumping:
            self.image = self.__movement_frames[3]
            self.__height_change = self.__jump_height
            self.__is_jumping = True
        
        
        
   
        
        
    def power_up_picked_up(self, new_power_up):
        """
        Called when a power up is picked up to set the current player power ups
        
        The power_ups list is implemented like a queue of size two. When the 
            queue is at max size, it pushes out the oldest power_up and 
            appends the new_power_up.
        
        Returns the id of the removed power up or, if there was not a power 
            up that was removed, 0.
        
        Args:
            new_power_up(int): integer id of the power up that was picked up.    
        """
        
        print ('picked up power up')
        
        if len(self.__power_ups) == 2:
            removed_power_up = self.__power_ups.pop(0)
        else:
            removed_power_up = 0
        self.__power_ups.append(new_power_up)
        return removed_power_up
        
    def slow(self):
        """
        Reduces the run_speed and jump_speed_modifier. 
        
        The run_speed_modifier is a constant value so the changes in speed are
            uniform.
            
        current_frame_reference must be within a certain bound in the run()
            method. Changing the run_speed can cause current_frame_reference
            to go out of bounds. current_frame_reference is reinstantiated to a
            value that will be within the bound:
            0 =< x < 3(number of frames) * run_speed
            based off of the current frame before this method is called.
        
        """
        
        self.__run_speed += self.__run_speed_modifier
        
        self.__current_frame_reference = self.__current_frame * self.__run_speed
        
#         self.__gravity = .5
        
    def speed_up(self):
        """
        Increases the run_speed and jump_speed_modifier.
        
        The run_speed_modifier is a constant value so the changes in speed are
            uniform.
            
        current_frame_reference must be within a certain bound in the run()
            method. Changing the run_speed can cause current_frame_reference
            to go out of bounds. current_frame_reference is reinstantiated to a
            value that will be within the bound:
            0 =< x < 3(number of frames) * run_speed
            based off of the current frame before this method is called. 
        """
        
        self.__run_speed -= self.__run_speed_modifier
        
        self.__current_frame_reference = self.__current_frame * self.__run_speed
        
#         self.__gravity = 2
        
    def update(self):
        """
        Updates the current image, and image location of the player.
        
        Calculate_gravity() is called if the player is jumping otherwise the 
            the run() function is called. 
            
        Note: This method is called every time a pygame.sprite.Group().update 
            method, that this player is apart of, is called.
        """
        
#         print ('update')
        if self.__is_jumping:
            self.__calculate_gravity()
        else:
            self.__run()
        
    
    
    
    def __calculate_gravity(self):
        """
        Causes the character to move towards the ground after jumping.
        
        The height_change variable modifies the y location of the player. 
            Everytime this method is called, the height_change variable is 
            decremented until this method is not called(when the player reaches
            the floor). Height_change is set in the jump() function
            
        The jump_speed_modifier determines the speed in which the player jump
            which creates the illusion of slow motion.
        """
        print ('calculate_gravity')
        
        # TODO: change bottom boundary
        if self.rect.y > 350:  # floor reached
            self.rect.y = 350
            self.__is_jumping = False
            self.image = self.__movement_frames[2]
            self.__height_change = 0
            print (self.__highest)
            self.__highest.sort()
            print (self.__highest[0])
            print ('length: ' + str(len(self.__highest)))
        else:
            self.__height_change = self.__height_change + self.__gravity
            self.rect.y = (self.__height_change * self.__jump_speed_modifier 
                           + self.rect.y)
            print (self.__highest.append(self.rect.y))
            
    
    def __run(self):
        """
        Changes the Player's sprite image to make it look like it's running.
        
        Sets the next frame to display by first setting the bound to 3 * 
            run_speed (since there are 3 frames for the running animation) then
            incrementing the current_frame_reference and getting the modulus 
            bound of it. Set the current_frame_reference to this value. Divide
            current_frame_reference by run_speed then convert it to an integer.
            Since current_frame_reference was created using the modulus of a 
            number 3 times run_speed, then the answer of current_frame_reference
            divided by run_speed will be a double between 0 inclusive and 
            exclusive 3. Since the previous answer will be a double and is then 
            converted to an int, it will truncate the value giving us any one 
            value: 0, 1 or 2.
        """
        # TODO: add run_speed_modifier
        bound = self.__run_speed * 3
        self.__current_frame_reference = (self.__current_frame_reference +
                                           1) % bound
        frame = int(self.__current_frame_reference / self.__run_speed)
        self.__current_frame = frame
        self.image = self.__movement_frames[frame]
      