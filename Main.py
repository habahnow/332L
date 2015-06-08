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
    
    

def generate_background(width, height, speed):
    """
    Method that generates the background
    
    Args:
        width: is the width of the screen.
        height: height of the screen
        speed: speed of the layers' movement.
        
    This method is hard coded to generate the background/platforms that the 
        Player is running on. It uses specific images in specific locations as 
        well as setting the location of the platforms and the initial speed.
    """
    movement_speed1 = speed
    movement_speed2 = speed
    movement_speed3 = speed
    
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
    
    # This value is used to slow down the number of times the layers update
    # if they are supposed to be going slow.
    update_counter = 0
    
     # Creating the ground layers.
    (layers, floor_locations) = generate_background(SURFACE_WIDTH, 
                                                    SURFACE_HEIGHT, -5)
    
    background_groups = layers.get_groups()
    
    # Generating groups
    enemies_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    powerups_group = pygame.sprite.Group()
    
    # Creating the player
    player = Player(10, 490, floor_locations)
    
    player_group.add(player)
    
    # Creating powerups and baddies.
    start_position = 1000
    
    # Generating ghosts
    active_ghosts = 0
    total_ghosts = 20
    ghost_list = []
    
    # Generating list for powerup reference.
    # 0 is the fast power up
    # 1 is the slow power up
    # 2 is the uppercut
    # 3 is the stomp power up
    power_up_reference_list = range(0, 4)
    
    
    # setting events for ghosts and powerups
    SPAWN_GHOST = USEREVENT + 1
    SPAWN_POWERUP = USEREVENT + 2
    TIMER = USEREVENT + 3 
    ACTIVE_TIME = USEREVENT + 4
    FAST_CD= USEREVENT + 5
    SLOW_CD = USEREVENT + 6
    UPPER_CUT_CD = USEREVENT + 7
    STOMP_CD = USEREVENT + 8
     
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
    powerup_spawn_time = random.randint(1000, 10000)
    
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
                    if not debugging:
                        print ('j released')
                    j_pressed = False
                if event.key == K_f:
                    if debugging:
                        print ('f released')
                    f_pressed = False
                if event.key == K_SPACE:
                    space_bar_pressed = False
            
            # Spawns a ghost after a certain interval.
            elif event.type == SPAWN_GHOST and not game_over:
                
                if not debugging:
                    print ('number of ghosts' + str( active_ghosts))
                    
                if active_ghosts <  total_ghosts:
                    ghost = Ghost(start_position, 
                                  floor_locations[random.randint(0,2)])
                    enemies_group.add(ghost)
                    ghost_list.append(ghost)
                    active_ghosts += 1
                enemy_spawn_time = random.randint(enemy_spawn_time_low, 
                                                  enemy_spawn_time_high)
                pygame.time.set_timer(SPAWN_GHOST, enemy_spawn_time)
                
                
                
            elif event.type == SPAWN_POWERUP and not game_over:
                # Change the spawn timer to a another random value. 
                powerup_spawn_time = random.randint(2000, 10000)
                pygame.time.set_timer(SPAWN_POWERUP, powerup_spawn_time)
                
                power_up_reference = power_up_reference_list[random.randint(0,
                                                                            3)]
                power_up_reference = 1
                if power_up_reference == 0:
                    if not debugging:
                        print ('PU is 0')
                     
                    # Create instance of powerup in random floor.
                    fast = Fast(start_position, 
                                floor_locations[random.randint(0,2)])
                    
                    powerups_group.add(fast)
                    

                elif power_up_reference == 1:
                    if debugging:
                        print ('PU is 1')
                        
                    # Create instance of powerup in random floor.
                    slow = Slow(start_position, 
                                floor_locations[random.randint(0,2)])
                    
                    powerups_group.add(slow)
                        
                elif power_up_reference == 2:
                    if debugging:
                        print ('PU is 2')
                        
                    # Create instance of powerup in random floor.
                    uppercut = UpperCut(start_position, 
                                floor_locations[random.randint(0,2)])
                    
                    powerups_group.add(uppercut)
                        
                elif power_up_reference == 3:
                    if debugging:
                        print ('PU is 3')
                       
                    # Create instance of powerup in random floor.
                    stomp = Stomp(start_position, 
                                floor_locations[random.randint(0,2)])
                    
                    powerups_group.add(stomp)   
                     
            # This is called every second to increase the score
            elif event.type == TIMER and not game_over:
                
                # Halves the amount of points gained from movement if player
                # if moving slow. This section increments the points if the 
                # player is slow and update counter is even or if the player is
                # not slow.
                if (player.is_slow and update_counter % 2 == 1 or 
                        not player.is_slow):
                    points_from_time += 10
                
                # Doubles the points gained from moving if the player is 
                # running fast.
                if player.is_fast:
                    points_from_time += 10
                
                if (points_from_time > interval_of_difficulty_increase):
                    interval_of_difficulty_increase += 150
                    if enemy_spawn_time_low >= 200:
                        enemy_spawn_time_low -= 100
                        enemy_spawn_time_high -= 100
                    
                    if not debugging:
                        print ('low: ' + str(enemy_spawn_time_low))
                        print ('high: ' + str(enemy_spawn_time_high))
                        
            elif event.type == FAST_CD:
                if debugging:
                    print ('cool_down done')
                pygame.time.set_timer(FAST_CD, 0)
                player.fast_on_cd = False
                
                
            elif event.type == SLOW_CD:
                if debugging:
                    print ('cool_down done')
                pygame.time.set_timer(SLOW_CD, 0)
                player.slow_on_cd = False
                
            elif event.type == UPPER_CUT_CD:
                if debugging:
                    print ('cool_down done')
                pygame.time.set_timer(UPPER_CUT_CD, 0)
                player.upper_cut_on_cd = False
                
            elif event.type == STOMP_CD:
                if debugging:
                    print ('cool_down done')
                pygame.time.set_timer(STOMP_CD, 0)
                player.stomp_on_cd = False
                
            elif event.type == ACTIVE_TIME:
                if debugging:
                    print ("active time done")
                pygame.time.set_timer(ACTIVE_TIME, 0)
                player.normalize_speed()
                


                    
        
        # Remove active ghosts that are out of view of the screen from the 
        # ghost list.
        for ghost in ghost_list:
            if ghost.rect.right <= 0:
                enemies_group.remove(ghost)
                ghost_list.remove(ghost)
                active_ghosts -= 1
                points_from_ghosts += 5
                
        # Remove power ups that are not in the screen view
        for powerup in powerups_group:
            if powerup.rect.right <= 0:
                powerups_group.remove(powerup)
                
        if space_bar_pressed:
            # If the player is in the game over screen, then replay game
            if game_over:
                game_over = False
                points_from_time = 0
                points_from_ghosts = 0
                ghost_list[:] = []
                enemies_group.empty()
                powerups_group.empty()
                active_ghosts = 0
                enemy_spawn_time_low = 1000
                enemy_spawn_time_high = 1500
            else:
                player.jump()
                
        if f_pressed:
            player.drop_down()
            
        if j_pressed:
            
            # Call user_power_up, from player, passing the id of the button(0).
            # If the power_up is slow or fast, then the called method will make
            # the speed change.
            ( active_time, 
              power_up_reference, power_up_used ) = player.use_power_up(0)
            
            # If the power_up used is slow or fast(has active time) and the 
            # player is not already using one of the two, then set the active 
            # timer.
            if active_time and power_up_used:
                if debugging:
                    print ('active timer set')
                pygame.time.set_timer(ACTIVE_TIME, active_time)
            
            # If the power_up was used, which includes all power_ups, call its
            # event timer.
            if power_up_used:
                if power_up_reference == 0:
                    pygame.time.set_timer(FAST_CD, 15000)
                    player.fast_on_cd = True

                elif power_up_reference == 1:
                    pygame.time.set_timer(SLOW_CD, 15000)
                    player.slow_on_cd = True
                    update_counter = 0
                    
                elif power_up_reference == 2:
                    pygame.time.set_timer(UPPER_CUT_CD, 2000)
                    player.upper_cut_on_cd = True
                    
                elif power_up_reference == 3:
                    pygame.time.set_timer(STOMP_CD, 2000)
                    player.stomp_on_cd = True
        
        if not game_over:
            SURFACE.fill(pygame.Color(4, 66, 13))
             
            # Updates and draws the background
            for group in background_groups:
                update_counter += 1
                if (player.is_slow and update_counter % 2 == 1 or 
                        not player.is_slow):
                    group.update()
                if player.is_fast:
                    group.update()
                group.draw(SURFACE)
            
            # Draw the enemies, player and powerups
            # Halves the speed of the powerups if the player
            # if moving slow. This section moves the powerups if the 
            # player is slow and update counter is even or if the player is
            # not slow.
            if (player.is_slow and update_counter % 2 == 1 or 
                    not player.is_slow):
                powerups_group.update()
            if player.is_fast:
                powerups_group.update()
            powerups_group.draw(SURFACE)
            
            # Halves the speed of the enemy sprites if player
            # is moving slow. This section moves the enemy sprites if 
            # player is slow and update counter is even or if the player is
            # not slow.
            if (player.is_slow and update_counter % 2 == 1 or 
                    not player.is_slow):
                enemies_group.update()    
            if player.is_fast:
                enemies_group.update()
            enemies_group.draw(SURFACE)
            
            # Halves the speed of the powerups if the player
            # if moving slow. This section moves the powerups if the 
            # player is slow and update counter is even or if the player is
            # not slow.
            if (player.is_slow and update_counter % 2 == 1 or 
                    not player.is_slow):
                player_group.update()
            if player.is_fast:
                player_group.update()
            player_group.draw(SURFACE)
            
            
             
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
            enemy_collisions = pygame.sprite.spritecollide(player, enemies_group,
                                                      True)
            
            # Check if player collides with powerup.
            power_up_collisions = pygame.sprite.spritecollide(player, 
                                                              powerups_group, True)
            
            # Check if the Player picks up a powerup.
            if power_up_collisions:
                player.power_up_picked_up(power_up_collisions[0].id)
            
            # Check if the player collides with an enemy. If so, pause game for
            # second then go to game_end screen
            if enemy_collisions:
                pygame.time.wait(500)
                game_over = True
                game_end(points_from_time + points_from_ghosts, SURFACE)
                
            
            
        fps_clock.tick(FPS)
    
                
        pygame.display.update()
        
if __name__ == "__main__":
    main()
        
