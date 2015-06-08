import os
import pygame
import sys 
from background import ParallaxLayer
from background import ParallaxLayers
from Ghost import Ghost 
from Power_ups import Fast, Slow, Stomp, UpperCut
from Player import Player
from pygame.locals import *
import random


debugging = True

def game_end(points, surface):
    # clear screen
    surface.fill(pygame.Color(4, 66, 13))
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 60, False, False)
    
    scoring_text = 'Final Score: ' + str(points)
    replay_text = 'Game OVER, press the space bar to play again'

    end_game_points = font.render( scoring_text, False, (200, 0, 0))
    game_over = font.render( replay_text, False, (200, 0, 0))
    
    (not_used, total_height) = font.size(scoring_text)
    
    (width, temporary_height) = font.size(replay_text)
    
    padding = 40
    
    total_height += temporary_height + padding
    
    width += padding
    
    pygame.draw.rect(surface, (0, 0, 100),(25, 340, width, total_height) )
    
    surface.blit(end_game_points,(350, 350))
    surface.blit(game_over,(50,410))
    
    

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
    movement_speed2 = -5
    movement_speed3 = -5
    
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
    enemy_list = pygame.sprite.Group()
    active_player = pygame.sprite.Group()
    player = Player(10, 490, floor_locations)
    
    active_player.add(player)
    
    # Creating powerups and baddies.
    start_position = 1000
    
    # Generating ghosts
    active_ghosts = 0
    total_ghosts = 20
    ghost_list = []
    
    
    # setting events for ghosts and powerups
    SPAWN_GHOST = USEREVENT + 1
    SPAWN_POWERUP = USEREVENT + 2
    TIMER = USEREVENT + 3 #TODO:
     
    # Instantiate point variables
    points_from_time = 0
    points_from_ghosts = 0
    
    # Interval in point value of how often the time for ghost respawn is 
    # reduced. Used in Timer event.
    interval_of_difficulty_increase = 150
    
    game_over = False
    
    # Setting up the font
    pygame.font.init() 
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 30, False, False)

    text_surface = font.render( str(points_from_time), False, (4, 66, 13))
    SURFACE.blit(text_surface,(800, 20))

    
    # Setting the initial spawn times for enemies and powerups
    enemy_spawn_time = random.randint(2000, 4000)
    powerup_spawn_time = random.randint(5000, 10000)
    
    enemy_spawn_time_low = 1000
    enemy_spawn_time_high = 1500
    
    pygame.time.set_timer(SPAWN_GHOST, enemy_spawn_time)
    pygame.time.set_timer(SPAWN_POWERUP, powerup_spawn_time)
    pygame.time.set_timer(TIMER, 1000) #TODO:
    
    
    
    j_pressed = False
    f_pressed = False
    space_bar_pressed = False
    
   
    
    while True: 
        for event in pygame.event.get():    
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_j:
                    if debugging:
                        print ('j pressed')
                    j_pressed = True
                if event.key == K_f:
                    if debugging:
                        print ('f pressed')
                    f_pressed = True
                if event.key == K_SPACE:
                    space_bar_pressed = True
                    
            if event.type == KEYUP:
                if event.key == K_j:
                    if debugging:
                        print ('j released')
                    j_pressed = False
                if event.key == K_f:
                    if debugging:
                        print ('f released')
                    f_pressed = False
                if event.key == K_SPACE:
                    space_bar_pressed = False
            
            # Spawns a ghost after a certain interval
            elif event.type == SPAWN_GHOST and not game_over:
                
                if debugging:
                    print ('number of ghosts' + str( active_ghosts))
                    
                if active_ghosts <  total_ghosts:
                    ghost = Ghost(start_position, 
                                  floor_locations[random.randint(0,2)])
                    enemy_list.add(ghost)
                    ghost_list.append(ghost)
                    active_ghosts += 1
                enemy_spawn_time = random.randint(enemy_spawn_time_low, 
                                                  enemy_spawn_time_high)
                pygame.time.set_timer(SPAWN_GHOST, enemy_spawn_time)
                
                
                
            elif event.type == SPAWN_POWERUP: #TODO
                a = 1
            
            # This is called every second to increase the score
            elif event.type == TIMER:
                points_from_time += 10
                if (points_from_time > interval_of_difficulty_increase):
                    interval_of_difficulty_increase += 150
                    if enemy_spawn_time_low >= 200:
                        enemy_spawn_time_low -= 100
                        enemy_spawn_time_high -= 100
                    
                    if debugging:
                        print ('low: ' + str(enemy_spawn_time_low))
                        print ('high: ' + str(enemy_spawn_time_high))
                        
                
        
        # Remove active ghosts that are out of view of the screen from the 
        # ghost list.
        for ghost in ghost_list:
            if ghost.rect.right <= 0:
                enemy_list.remove(ghost)
                ghost_list.remove(ghost)
                active_ghosts -= 1
                points_from_ghosts += 5

        if space_bar_pressed:
            # If the player is in the game over screen, then replay game
            if game_over:
                game_over = False
                points_from_time = 0
                ghost_list[:] = []
                enemy_list.empty()
                active_ghosts = 0
                enemy_spawn_time_low = 1000
                enemy_spawn_time_high = 1500
            else:
                player.jump()
        if f_pressed:
            player.drop_down()
        
        if not game_over:
            SURFACE.fill(pygame.Color(4, 66, 13))
             
            # Updates and draws the background
            for group in background_groups:
                group.update()
                group.draw(SURFACE)
            
            # Draw the enemies and player
            enemy_list.update()    
            enemy_list.draw(SURFACE)
             
            active_player.update()
            active_player.draw(SURFACE)
             
            # Display Scoring
            score_text = 'Points: ' + str(points_from_time + points_from_ghosts)
            padding = 10
            (width, height) = font.size(score_text)
            text_surface = font.render( score_text, False, (0, 0, 0), 
                                       (200, 0, 0))
            width += padding
            height += padding
            pygame.draw.rect(SURFACE, (200, 0, 0),(795, 15, width, height))
            SURFACE.blit(text_surface, (800, 20))
     
             
            # check if player collides with ghosts.
            enemy_collisions = pygame.sprite.spritecollide(player, enemy_list,
                                                      True)
            
            # Check if the player collides with an enemy. If so, pause game for
            # second then go to game_end screen
            if enemy_collisions:
                pygame.time.wait(1000)
                game_over = True
                game_end(points_from_time + points_from_ghosts, SURFACE)
            
            
        fps_clock.tick(FPS)
    
                
        pygame.display.update()
        
if __name__ == "__main__":
    main()
        
