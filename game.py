import pygame
import sys


from grid import Grid
from player import Player
from stats import Stats


class Button:
    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen):

        button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, "dimgrey", button_rect, border_radius=5)

        text_surface = self.font.render(self.text, True, "white")
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def draw_large(self, screen):
        """Draws the button with a larger text size."""
        button_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, "dimgrey", button_rect, border_radius=5)

        large_font = pygame.font.SysFont("Arial", 15)  # Bigger font for emphasis
        text_surface = large_font.render(self.text, True, "white")
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        """Check if the button was clicked."""
        return self.x <= mouse_pos[0] <= self.x + self.w and self.y <= mouse_pos[1] <= self.y + self.h

class Game:
    def __init__(self, grid_width, grid_height, player_positions, stats=None, cell_size=40, selection_func=None):
        pygame.init()
        self.grid = Grid(grid_width, grid_height, cell_size)
        self.stats = stats if stats else Stats()# Initialize stats tracking
        self.stats.start_timer()  # Start the timer when the game begins
        window_width = grid_width * cell_size
        window_height = grid_height * cell_size
        self.selection_func = selection_func
        self.screen = pygame.display.set_mode((window_width, window_height + 100))  # Extra space for stats
        pygame.display.set_caption("Wandering in the Woods")

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.players = [Player(i + 1, x, y, (grid_width, grid_height), colors[i], self.stats, cell_size)
                        for i, (x, y) in enumerate(player_positions)]

        self.groups = [[player] for player in self.players]

        self.font = pygame.font.SysFont("Arial", 24)  # Font for step counter



    def game_over(self): # displays game over text

        self.screen.fill((255, 255, 255))  # White background
        self.grid.draw(self.screen)  # Draw grid

        # show players in their final positions
        for player in self.players:
            pygame.draw.circle(
                self.screen,
                player.color,
                (player.x * self.grid.cell_size + self.grid.cell_size // 2,
                 player.y * self.grid.cell_size + self.grid.cell_size // 2),
                self.grid.cell_size // 2 - 5
            )

        # Define bottom area for text display
        text_offset_y = self.screen.get_height() - 80  # Adjusts text position near bottom

        # Show "Game Over" message near bottom
        game_over_text = self.font.render("Game Over!", True, (0, 0, 0))
        self.screen.blit(game_over_text, (self.screen.get_width() // 2 - 80, text_offset_y))

        if len(self.players) == 2 and self.grid.cols == 6 and self.grid.rows == 6:
            try:
                happy_image = pygame.image.load("fireworks.jpg").convert_alpha()  # Load image
                happy_image = pygame.transform.scale(happy_image, (300, 300))  # Resize if needed
                happy_image.set_alpha(50)
                self.screen.blit(happy_image, (self.screen.get_width() // 2 - 150, 50))  # Center image
            except pygame.error as e:
                print("Error loading image:", e)


        pygame.display.flip()
        pygame.time.delay(4000)  # Show for 4 seconds
        self.display_full_stats()  # Transition to full stats screen

    def check_collisions(self): # check if player have met

        merged_groups = []
        merged = set()

        # Loop through each group to check for collisions
        for i, group in enumerate(self.groups):
            if i in merged:
                continue  # Skip groups that have already merged

            new_group = set(group)  # Start with the current group

            for j, other_group in enumerate(self.groups):
                if i != j and any(p1.x == p2.x and p1.y == p2.y for p1 in new_group for p2 in other_group):
                    new_group.update(other_group)  # Merge the two groups
                    merged.add(j)  # Mark this group as merged

            # Add the new merged group to the list
            merged_groups.append(list(new_group))

        self.groups = merged_groups  # Update groups

        # k-2 ends when the players meet
        if len(self.players) == 2 and len(self.groups) == 1:
            print("Players met!")
            if len(self.players) == 2 and len(self.groups) == 1:
                print("K-2: Players met!")

                self.stats.stop_timer()  # Stop the timer when the game ends
                self.stats.save_stats()  # Save stats
                self.game_over()
                return


        #  3-5 and 6-8: continue until all players are together
        elif len(self.groups) == 1 and len(self.groups[0]) == len(self.players):
            print("All players have found each other!")

            self.stats.stop_timer()  # Stop the timer when the game ends
            self.stats.save_stats()  # Save stats before showing
            self.game_over()

            self.display_full_stats()



    def display_full_stats(self):


        self.screen.fill((255, 255, 255))  # White background
        #stats_font = pygame.font.SysFont('Verdana', 16)


        # Display Total Steps for all grade levels
        total_steps_text = f"Total Steps: {self.stats.get_total_steps()}"
        step_surface = self.font.render(total_steps_text, True, (0, 0, 0))
        self.screen.blit(step_surface, (self.screen.get_width() // 2 - 80, 80))

        # Check if the game was played in K-2 mode (2 players, fixed grid)
        if len(self.players) == 2 and self.grid.cols == 6 and self.grid.rows == 6:
            # K-2 mode: Only display total steps
            pygame.display.flip()
            pygame.time.delay(5000)  # return to main menu after 5 seconds
            from Main import main_game_gui
            main_game_gui()  # return to main menu
            return

        # stats for 3-5 and 6-8
        longest_run_text = f"Longest Run: {self.stats.get_longest_run()} sec"
        shortest_run_text = f"Shortest Run: {self.stats.get_shortest_run()} sec"
        average_run_text = f"Average Run: {self.stats.get_average_run_time()} sec"


        longest_surface = self.font.render(longest_run_text, True, (0, 0, 0))
        shortest_surface = self.font.render(shortest_run_text, True, (0, 0, 0))
        average_surface = self.font.render(average_run_text, True, (0, 0, 0))

        self.screen.blit(longest_surface, (self.screen.get_width() // 2 - 100, 140))
        self.screen.blit(shortest_surface, (self.screen.get_width() // 2 - 100, 180))
        self.screen.blit(average_surface, (self.screen.get_width() // 2 - 100, 220))

        play_again_button = Button(self.screen.get_width() // 2 - 100, 270, 90, 40, "Play Again")
        main_menu_button = Button(self.screen.get_width() // 2 + 10, 270, 90, 40, "Main Menu")

        play_again_button.draw_large(self.screen)
        main_menu_button.draw_large(self.screen)

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if "Play Again" button is clicked
                    if play_again_button.x <= mouse_pos[0] <= play_again_button.x + play_again_button.w and \
                            play_again_button.y <= mouse_pos[1] <= play_again_button.y + play_again_button.h:



                        if self.selection_func:
                            print(
                                f"🔄 Restarting with grid size ({self.grid.cols}, {self.grid.rows}) and {len(self.players)} players.")
                            self.selection_func(self.grid.cols, self.grid.rows, len(self.players))

                        return


                    # Check if "Main Menu" button is clicked
                    if main_menu_button.x <= mouse_pos[0] <= main_menu_button.x + main_menu_button.w and \
                            main_menu_button.y <= mouse_pos[1] <= main_menu_button.y + main_menu_button.h:
                        print("Returning to Main Menu...")
                        from Main import main_game_gui
                        main_game_gui()
                        return

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill((50, 50, 50,))  #  background grid color during game
            self.grid.draw(self.screen)  # Draw grid

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Move each group together
            for group in self.groups:
                leader = group[0]  # The leader moves first
                leader.move()


                #  group members follow leader
                for player in group[1:]:
                    player.x, player.y = leader.x, leader.y

                    # Increment overall game step counter once per move
                self.stats.increment_steps()
                print(f"Total Steps: {self.stats.get_total_steps()}")  # Debug output

            self.check_collisions()  # check for player meetings

            # Draw players
            for group in self.groups:
                for player in group:
                    pygame.draw.circle(
                        self.screen,
                        player.color,
                        (player.x * self.grid.cell_size + self.grid.cell_size // 2,
                         player.y * self.grid.cell_size + self.grid.cell_size // 2),
                        self.grid.cell_size // 2 - 5
                    )

            pygame.display.flip()
            clock.tick(10)  # player movement speed

        pygame.quit()
        sys.exit()


### INITIAL COMMENTS ###

#Wandering in the Woods Game

# ABOUT THE GAME

#Stored in: 
#Created by: Ruby Radosevic, Jasmine Davis, and Carlos Manzo
#Contact at: rubyaradosevic@lewisu.edu {JASMINE'S EMAIL} and cmanzo20@stu.jjc.edu
#Course: Software Engineering 44000 - LT1
#Completed on:{COMPLETION DATE}


### INITIALIZATIONS ###

import pygame as pg
import pygame_gui as pgg
import sys
import os

pg.init()
pg.font.init()

main_font = pg.font.SysFont('Verdana', 10)
large_font = pg.font.SysFont('Verdana',18)
x_large_font = pg.font.SysFont('Verdana',32)

### CLASS CREATIONS ###

## Class for each player object
class player():
    ## Constructor for player with x coord, y coord, and player id
    def __init__(self, player_id, x, y):
        self.player_id = player_id
        self.x=x
        self.y=y
    
    ## Function for handling player movement- may need to be changed based on game mechanics
    def move(self, direction):
        if direction== "up":
            self.y +=1
        elif direction=="down":
            self.y -=1
        elif direction=="left":
            self.x -=1
        elif direction=="right":
            self.x+=1

    ## returns players current coordinates
    def getCoords(self):
        return (self.x, self.y)
    
    ## Sets players coordinates
    def setCoords(self, x, y):
        self.x = x
        self.y = y

## Button Class for easy button and text drawing onto page ##
class Button():         
    def __init__(self, x, y, w, h, text):
        self._x = x
        self._y = y
        self._h = h
        self._w = w
        self._text = text


    def draw(self, window):   #Draws rectangle of w width and h height at (x,y)
        button_image = pg.Rect(self._x, self._y, self._w, self._h)
        pg.draw.rect(window, ("dimgrey"), button_image, width = 3, border_radius=5)
        display_text = main_font.render(self._text, False, color = "dimgrey")         #Draws text onto button
        window.blit(display_text, (self._x+7, self._y+3))


    def draw_large(self, window):   #Draws rectangle of w width and h height at (x,y) with larger text
        button_image = pg.Rect(self._x, self._y, self._w, self._h)
        pg.draw.rect(window, ("dimgrey"), button_image, width = 3, border_radius=5)
        display_text = large_font.render(self._text, False, color = "dimgrey")         #Draws text onto button
        window.blit(display_text, (self._x+7, self._y+3))



### FUNCTION CREATIONS ###

## Simple function that returns True if 2 coordinates have the same values ##
def check_coords(coord1, coord2):           
    return (coord1 == coord2)

# Function for playing specified audio file in AudioFiles folder
def play_audio_file(fileName):
    pg.mixer.init()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    mp3_file_path = os.path.join(current_directory, "AudioFiles" , fileName)

    #checks if audio is already playing
    if pg.mixer.music.get_busy():
        pg.mixer.music.stop()  # Stop any music that might already be playing

    try:
        # Load and play MP3 file once
        pg.mixer.music.load(mp3_file_path)
        pg.mixer.music.play(loops=0)

    except Exception as e:
        print(f"Error loading or playing the file: {e}")
    return None

### WINDOW CREATIONS ###

## About Window function creates a new screen that displays basic information about how the game is played ##
def about_window():
    about_screen = pg.display.set_mode((325,325))   #Initializes the window and background
    pg.display.set_caption("How to Play")
    background = pg.Surface((325,325))
    background.fill("whitesmoke")
    about_screen.blit(background,(0,0))

    return_button = Button(225,25,75,25, "Main Menu")   #Creates button to return to the main menu and About text
    return_button.draw(about_screen)

    About = [   # Short game Description
        "Wandering in the Woods is a game where players are",
        "simulated wandering through the dark and ominous woods.",
        "It is very dark in the woods, so you must wander",
        "aimlessly. How long will it take to find your friends?"
    ]

    How_to_Play = [ # How to play- susceptible to change
        "How to Play:",
        "1. Select the complexity (K-2, 3-5, 6-8).",
        "2. Select the grid size and number of players (2-5 and up).",
        "3. Select each player's starting coordinates (2-5 and up)",
        "4. Watch as players wander aimlessly through the woods.",
        "5. The goal is to reach all of your friends in the woods.",
        "6. Have fun and good luck!"
    ]

    # Draw the text
    y_offset = 60  # Start position for the first line of text 
   
    for line in About:
        text_surface = main_font.render(line, True, (0,0,0))
        about_screen.blit(text_surface, (20, y_offset))
        y_offset+=10
    
    y_offset+=20 # Extra spacing between how to play 

    for line in How_to_Play:  ## Loop that prints each line in how to play txt
        text_surface = main_font.render(line, True, (0, 0, 0))  # Black color for text
        about_screen.blit(text_surface, (20, y_offset))  # Draw text with an offset
        y_offset += 30  # Increase y position for the next line of text

    # Update the display
    pg.display.flip()
    play_audio_file("About.mp3")
    
    running = True
   
    while running:

        events = pg.event.get() #The same loop is used for every window; every display refresh gets events
        for event in events:
            if event.type == pg.QUIT:   #No longer running if x-ed out 
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:    #The same event type is used to check for user mouse clicks
                mouse_pos = pg.mouse.get_pos()  

                if (250 <= mouse_pos[0] <=300) and (25 <= mouse_pos[1] <= 50):  #The same if-statement is used to check for button clicks
                    running = False   #No longer running if Main Menu Button is pressed

        pg.display.update()
    main_game_gui()     #Runs the Main Game function and returns to main menu when no longer running

## Selection Window function creates a new screen where players select the width and height of the grid (between 1 and 20) ##
## as well as selects between 2, 3, and 4 players before moving onto the next set of selections ##
def selection_window():
    str_item_list = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]    #Value inits
    grid_width_bool = False
    grid_height_bool = False
    player_number_bool = False

    selection_screen = pg.display.set_mode((400,300))   #Screen inits
    pg.display.set_caption("Gameplay Selection")
    background = pg.Surface((400,300))
    background.fill("whitesmoke")
    selection_screen.blit(background,(0,0))
    pgmanager = pgg.UIManager((400,300))    #Manager to check for UI selection list selections
    selection_clock = pg.time.Clock()
    refresh = selection_clock.tick(60)/1000
    width_text = large_font.render("Grid Width", False, color = "dimgrey")  #Text inits
    selection_screen.blit(width_text, (25,75))    
    height_text = large_font.render("Grid Height", False, color = "dimgrey")
    selection_screen.blit(height_text, (150,75)) 
    player_text = large_font.render("# of Players", False, color = "dimgrey")
    selection_screen.blit(player_text, (265,75))     

    #Creates 3 UI selection lists of allowed integer values for grid width, grid height, and # of players respectively
    width_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(25, 100, 100, 125), item_list=str_item_list, manager = pgmanager, object_id = "grid_width")
    height_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(150, 100, 100, 125), item_list=str_item_list, manager = pgmanager, object_id="grid_height")
    player_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(275, 100, 100 ,65), item_list=["2", "3", "4"], manager = pgmanager, object_id="player_number")
 
    continue_button = Button(275,175,100,50,"Continue") #Button init
    continue_button.draw_large(selection_screen)

    play_audio_file("SelectPrompt.mp3")

    running = True

    while running:

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:   #Returns to main menu if x-ed out
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                #Continues to next selection screen if all 3 selectinos have been made, and the continue button has been pressed
                if grid_width_bool and grid_height_bool and player_number_bool and (275 <= mouse_pos[0] <= 375) and (175 <= mouse_pos[1] <= 225):
                    grid_and_player_selection(int(grid_width), int(grid_height), int(player_number))

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (25 <= mouse_pos[0] <= 125): #Uses same elif statement where
                grid_width = event.text                            # events of new list selection type at correct UI box location 
                grid_width_bool = True                             # updates appropriate variable as well as changes a bool to True
                print(event.text)                                  # to make sure all necessary selections have been made

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (150 <= mouse_pos[0] <= 250):
                grid_height = event.text
                grid_height_bool = True
                print(event.text)

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (275 <= mouse_pos[0] <= 375):
                player_number = event.text
                player_number_bool = True
                print(event.text)

            pgmanager.process_events(event) #Used for pygame GUI events

        pgmanager.update(refresh)   #Refreshes pgmanager with display update
        pgmanager.draw_ui(selection_screen)    #Draws UI selection lists
        pg.display.update()

    main_game_gui()


## Grid and Player Selection function creates a new window that takes in previously selected grid width, height, and # of players ##
## and lets the user pick where each player will be starting on the grid ##
def grid_and_player_selection(grid_width, grid_height, number_of_players):

    str_grid_width_list = []    #Variable inits
    str_grid_height_list = []
    player_1_x_bool = False
    player_1_y_bool = False
    player_2_x_bool = False
    player_2_y_bool = False    
    player_3_x_bool = False
    player_3_y_bool = False
    player_4_x_bool = False
    player_4_y_bool = False

    selection_screen = pg.display.set_mode((375,200 + 100 * number_of_players))   #Screen inits
    pg.display.set_caption("Gameplay Selection")
    background = pg.Surface((375,200 + 100 * number_of_players))
    background.fill("whitesmoke")
    selection_screen.blit(background,(0,0))
    pgmanager = pgg.UIManager((375,200 + 100 * number_of_players))    #GUI manager inits
    selection_clock = pg.time.Clock()
    refresh = selection_clock.tick(60)/1000
    matching_coords_text = large_font.render("Player coordinates cannot match!", None, color = "dimgrey") #Text init for later

    start_button = Button(250,150 + 100 * number_of_players,90,40,"Start!")   #Start Button init
    start_button.draw_large(selection_screen)

    for j in range(grid_width):     #Creates UI-usable list based on user-selected grid width
        str_grid_width_list.append(str(j+1))

    for k in range(grid_height):       #Creates UI-usable list based on user-selectec grid height
        str_grid_height_list.append(str(k+1))


    for player in range(number_of_players):     #Displays text based on the number of players
        display_text = large_font.render(("Player " + str(player+1)), False, color = "dimgrey")
        selection_screen.blit(display_text, (25, 150 + (100 * player)))

        # Based on number of players, 2 UI selection lists are created for x- and y-locations of each player, using above lists
        if player == 0:
            player_1_x_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(150, 150, 90, 90), item_list=str_grid_width_list, manager = pgmanager, object_id = "player_1_x")
            player_1_y_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(250,150,90,90), item_list=str_grid_height_list, manager=pgmanager, object_id="player_1_y")

        if player == 1:
            player_2_x_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(150, 250, 90, 90), item_list=str_grid_width_list, manager = pgmanager, object_id = "player_2_x")
            player_2_y_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(250,250,90,90), item_list=str_grid_height_list, manager=pgmanager, object_id="player_2_y")

        if player == 2:
            player_3_x_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(150, 350, 90, 90), item_list=str_grid_width_list, manager = pgmanager, object_id = "player_3_x")
            player_3_y_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(250,350,90,90), item_list=str_grid_height_list, manager=pgmanager, object_id="player_3_y")

        if player == 3:
            player_4_x_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(150, 450, 90, 90), item_list=str_grid_width_list, manager = pgmanager, object_id = "player_4_x")
            player_4_y_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(250,450,90,90), item_list=str_grid_height_list, manager=pgmanager, object_id="player_4_y")

    if number_of_players < 3:   #Sets player 3 and 4 bools to True if only 2 players (necessary for Start Button)
        player_3_x_bool = True
        player_3_y_bool = True       

    if number_of_players < 4:   #Sets player 4 bools to True if only 3 players (necessary for Start Button)
        player_4_x_bool = True
        player_4_y_bool = True            

    play_audio_file("SelectCoords.mp3")

    running = True
    while running:

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                if (250 <= mouse_pos[0] <= 340) and (550 <= mouse_pos[1] <= 590):

                    if player_1_x_bool and player_1_y_bool and player_2_x_bool and player_2_y_bool and\
                    player_3_x_bool and player_3_y_bool and player_4_x_bool and player_4_y_bool:    #Only checks if game can start
                                                                                       #if all necessary selections have been made
                        if number_of_players < 3:   #Checks player 1 and 2 coords to see if they match

                            if check_coords((player_1_x,player_1_y),(player_2_x,player_2_y)):
                                selection_screen.blit(matching_coords_text, (40,75))    #Displays text saying coordinates cannot match

                            else:   #Game starts if no coordinates match
                                print("Game Start!")    
### FIX: SHOULD RUN GAME

                        elif number_of_players < 4:     #Checks player 1, 2 and 3 coords to see if they match

                            if check_coords((player_1_x,player_1_y),(player_2_x,player_2_y)):
                                selection_screen.blit(matching_coords_text, (40,75))

                            elif check_coords((player_1_x,player_1_y),(player_3_x,player_3_y)):
                                selection_screen.blit(matching_coords_text, (40,75))

                            elif check_coords((player_2_x,player_2_y),(player_3_x,player_3_y)):
                                selection_screen.blit(matching_coords_text, (40,75))
                            else:   #Game starts if no coordinates match
                                print("Game Start!")
### FIX: SHOULD RUN GAME

                        else:   #Checks player 1,2,3 and 4 coords to see if they match
                            if check_coords((player_1_x,player_1_y),(player_2_x,player_2_y)):
                                selection_screen.blit(matching_coords_text, (40,75))

                            elif check_coords((player_1_x,player_1_y),(player_3_x,player_3_y)):
                                selection_screen.blit(matching_coords_text, (40,75))

                            elif check_coords((player_2_x,player_2_y),(player_3_x,player_3_y)):
                                selection_screen.blit(matching_coords_text, (40,75))

                            elif check_coords((player_1_x,player_1_y),(player_4_x,player_4_y)):
                                selection_screen.blit(matching_coords_text, (40,75))       

                            elif check_coords((player_2_x,player_2_y),(player_4_x,player_4_y)):
                                selection_screen.blit(matching_coords_text, (40,75))

                            elif check_coords((player_3_x,player_3_y),(player_4_x,player_4_y)):
                                selection_screen.blit(matching_coords_text, (40,75))                                

                            else:   #Game starts if no coordinates match
                                print("Game Start!")
### FIX: SHOULD RUN GAME
                
            #Updates UI selection variable and bool based on mouse position for elif statements below
            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (150 <= mouse_pos[0] <= 240) and (150 <= mouse_pos[1] <= 240):
                player_1_x = event.text
                player_1_x_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (150 <= mouse_pos[0] <= 240) and (250 <= mouse_pos[1] <= 340):
                player_2_x = event.text
                player_2_x_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (150 <= mouse_pos[0] <= 240) and (350 <= mouse_pos[1] <= 440):
                player_3_x = event.text
                player_3_x_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (150 <= mouse_pos[0] <= 240) and (450 <= mouse_pos[1] <= 540):
                player_4_x = event.text
                player_4_x_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (250 <= mouse_pos[0] <= 340) and (150 <= mouse_pos[1] <= 240):
                player_1_y = event.text
                player_1_y_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (250 <= mouse_pos[0] <= 340) and (250 <= mouse_pos[1] <= 340):
                player_2_y = event.text
                player_2_y_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (250 <= mouse_pos[0] <= 340) and (350 <= mouse_pos[1] <= 440):
                player_3_y = event.text
                player_3_y_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (250 <= mouse_pos[0] <= 340) and (450 <= mouse_pos[1] <= 540):
                player_4_y = event.text
                player_4_y_bool = True

            pgmanager.process_events(event)

        pgmanager.update(refresh)
        pgmanager.draw_ui(selection_screen)
        pg.display.update()
    main_game_gui() #Runs Main Game function if x-ed out



## Main Game GUI Function is the main function that needs to be launched for the game to begin. Users select level, or can click ##
## About to see how the game works ##
def main_game_gui():

    game_creation_screen = pg.display.set_mode((325,500))   #Screen inits
    pg.display.set_caption("Main Menu | Wandering in the Woods")
    background = pg.Surface((325,500))
    background.fill("whitesmoke")
    game_creation_screen.blit(background,(0,0))
    display_text = x_large_font.render("Wandering", False, color = "dimgrey")   #Text inits
    game_creation_screen.blit(display_text, (75, 360))
    display_text_2 = x_large_font.render("in the", False, color = "dimgrey")
    game_creation_screen.blit(display_text_2,(115,400))
    display_text_3 = x_large_font.render("Woods", False, color = "dimgrey")
    game_creation_screen.blit(display_text_3,(107,440))

    K_though_2_button = Button(25,300,75,50,"K Through 2")  #Button inits
    K_though_2_button.draw(game_creation_screen)

    three_through_5_button = Button(125, 300, 75, 50, "3 Through 5")
    three_through_5_button.draw(game_creation_screen)

    six_through_8_button = Button(225, 300, 75, 50, "6 Through 8")
    six_through_8_button.draw(game_creation_screen)

    about_button = Button(250, 25, 50, 25, "About")
    about_button.draw(game_creation_screen)

# RRFIX: Create picture for main menu
    play_audio_file("Welcome.mp3") # Plays welcome audio when main menu is loaded

    running = True
    while running:

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                pg.quit()   #When the main menu is closed, pygame is quit and the program is terminated
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                if (25 <= mouse_pos[0] <= 100) and (300 <= mouse_pos[1] <= 350):
                    print("K through 2")
### FIX: SHOULD RUN GAME

                elif (125 <= mouse_pos[0] <= 200) and (300 <= mouse_pos[1] <= 350):
                    print("3 through 5")    #Launches 3-5 selection screen
                    selection_window()

                elif (225 <= mouse_pos[0] <= 300) and (300 <= mouse_pos[1] <= 350):
                    print("6 through 8")    #Launches 6-8 selection screen
                    selection_window()

                elif (250 <= mouse_pos[0] <= 300) and (25 <= mouse_pos[1] <= 50):
                    print("ABOUT")  #Launches about section
                    about_window()

        pg.display.update()
    return None

main_game_gui()
