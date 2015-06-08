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

debugging = True

class Player(pygame.sprite.Sprite):
    fast_on_cd = False
    slow_on_cd = False
    upper_cut_on_cd = False
    stomp_on_cd = False
    is_fast = False
    is_slow = False
    is_stomping = False
    is_uppercutting = False
    power_ups = []    
    __current_frame_reference = 2
    __current_frame = 0
    __current_floor = 0  
    __gravity = 1
    __height_change = 0 # Number of pixels to reduce height by.
    __level_changed = False 
    __is_jumping = False
    __is_falling = False 
    __regular_jump_height = -22
    __jump_speed_modifier = 1
    __movement_frames = [] # Contains the images for the sprite
    __run_speed = 8
    __run_speed_modifier = 5
    
    
    
    
    def __init__(self, x, y, floor_locations):
        """
        Initializes the player class using a passes x and y coordinate
        
        Args:
            x (int): the horizontal location of where the sprite will appear.
            y (int): the vertical location of where the sprite will appear.
            floor_locations(list): Contains the y coordinates of the different 
                floors. This reduces the amount of hard coding necessary, and 
                is used in to set the ground for the Player at different 
                floors.
            
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
        
        # Set the boundaries for the floors.
        self.__floor_boundaries = floor_locations
        
    
    def drop_down(self): 
        """
        The command that will make the Player drop down a floor.
        
        This method calls on the methods decrement floor to have the Player 
            drop a floor if the player is not at the lowest floor, or jumping 
            or already falling.
            
        
        """
        
        if not debugging:
            print ('drop down')
            
        if (not self.__is_jumping and not self.__is_falling and
                self.__current_floor != 0):
            self.image = self.__movement_frames[1]
            self.__decrement_floor()
            self.__is_falling = True
        
    def jump(self, jump_height=__regular_jump_height, normal_jump=True): 
        """
        Moves the character's y locations, making it look like it's jumping.
        
        Method checks if the player is jumping with the is_jumping variable. If
            player is not, then the image is changed to the jumping image and 
            the height_change variable is set.
        """
        
        if not debugging:
            print ('jump')
        
        if not self.__is_jumping and not self.__is_falling:
            self.image = self.__movement_frames[3]
            self.__height_change = jump_height
            self.__is_jumping = True
            
    def normalize_speed(self):
        self.__run_speed = 8
        self.is_fast = False
        self.is_slow = False
        
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
        if not debugging:
            print ('picked up power up')
        
        if len(self.power_ups) == 2:
            removed_power_up = self.power_ups.pop(0)
        else:
            removed_power_up = 0
        self.power_ups.append(new_power_up)
        return removed_power_up
        
    def slow_down(self):
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
        if not self.is_slow:
            self.is_slow = True
#         self.__run_speed += self.__run_speed_modifier
#         
#         self.__current_frame_reference = self.__current_frame * self.__run_speed
#         
# #         self.__gravity = .5
        
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
        if not self.is_fast:
            self.is_fast = True
#             self.__run_speed -= self.__run_speed_modifier
         
#             self.__current_frame_reference = self.__current_frame * self.__run_speed
        
        
    def update(self):
        """
        Updates the current image, and image location of the player.
        
        Calculate_gravity() is called if the player is jumping otherwise the 
            the run() function is called. 
            
        Note: This method is called every time a pygame.sprite.Group().update 
            method, that this player is apart of, is called.
        """
        
        if self.__is_jumping or self.__is_falling:
            self.__calculate_gravity()
        else:
            self.__run()
            
    def uppercut(self):
        if debugging:
            print ('uppercut')
        
    def use_power_up(self, key_id):
        """
            0 is the fast power up
            1 is the slow power up
            2 is the uppercut
            3 is the stomp power up
        """
        if len(self.power_ups) == 0:
            print ('no powerups')
            return (0,0,False)
        elif self.power_ups[key_id] == 0:
            if debugging:
                print ('power is 0')
                
            if not self.is_fast and not self.fast_on_cd:
                self.speed_up()
            
                # Return active time in milliseconds, power_up reference, and 
                # if the power_up was used.
                return (8000, 0, True)
            else:
                return (0, 0, False)
        
        elif self.power_ups[key_id] == 1:
            if debugging:
                print ('power is 1')
            
            if not self.is_slow and not self.slow_on_cd:
                self.slow_down()  
                
                return (8000, 1, True)
            else:
                return (0,1, False)
                
        elif self.power_ups[key_id] == 2:
            if debugging:
                print ('power is 2')
                
            if (not self.__is_jumping and not self.__is_falling and 
                    not self.is_stomping and not self.upper_cut_on_cd):
                self.uppercut()
                
                return (0, 2, True)
            else:
                return (0, 2, False)
                
        elif self.power_ups[key_id] == 3:
            if debugging:
                print ('power is 3')
            
            if (not self.__is_jumping and not self.__is_falling and 
                    not self.is_stomping and not self.stomp_on_cd):
                self.stomp()
                
                return (0, 3, True)
            else:
                return (0,3,False)
    
    
    def __calculate_gravity(self):
        """
        Causes the character to move towards the ground after jumping.
        
        Checks if the player rectangle is below the floor boundary of the 
            current floor. If it is, then the Player is set to the level of the 
            current floor. Otherwise, the Player gets brought down by gravity.
        
        The height_change variable modifies the y location of the player. 
            Everytime this method is called, the height_change variable is 
            decremented until this method is not called(when the player reaches
            the floor). Height_change is set in the jump() function
            
        The jump_speed_modifier determines the speed in which the player jump
            which creates the illusion of slow motion.
        """
        
        # if player is below floor boundary move above floor.
        if self.rect.y > self.__floor_boundaries[self.__current_floor]:
            
            self.rect.y = self.__floor_boundaries[self.__current_floor]
            self.__is_jumping = False
            self.__is_falling = False
            self.__level_changed = False
            self.image = self.__movement_frames[2]
            self.__height_change = 0
        # Else apply gravity.
        else:
            self.__height_change = self.__height_change + self.__gravity
            # if player is beginning to fall down/
            if (self.__height_change >= 0 and self.__is_jumping and 
                    not self.__level_changed):
                self.__increment_floor()
                self.__level_changed = True
            self.rect.y = (self.__height_change * self.__jump_speed_modifier 
                           + self.rect.y)
            
            
    def __decrement_floor(self): 
        """ 
        Decrements the floor that the player is on. 
        
        This method is called from other methods and helps to move the Player 
            a floor below the current one if it exists.
        
        Decrements the current_floor but sets it to 0 if it falls below 0.
        """
        
        if not debugging:
            print('decrement floor')
        self.__current_floor -= 1
        if self.__current_floor < 0:
            self.__current_floor = 0
            
    def __increment_floor(self): 
        """
        Increases the current floor of the Player.
        
        Increases the current_floor up to a maximum of 2.
        """
        if not debugging: 
            print ('increment floor')
        self.__current_floor += 1
        if self.__current_floor > 2:
            self.__current_floor = 2
    
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
        if not debugging:
            print ('run')
            
        bound = self.__run_speed * 3
        self.__current_frame_reference = (self.__current_frame_reference +
                                           1) % bound
        frame = int(self.__current_frame_reference / self.__run_speed)
        self.__current_frame = frame
        self.image = self.__movement_frames[frame]
      