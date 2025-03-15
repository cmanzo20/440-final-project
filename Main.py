### INITIAL COMMENTS ###

# Wandering in the Woods Game

# ABOUT THE GAME

# Stored in:
# Created by: Ruby Radosevic, Jasmine Davis, and Carlos Manzo
# Contact at: rubyaradosevic@lewisu.edu jasminesdavis@lewisu.edu and cmanzo20@stu.jjc.edu
# Course: Software Engineering 44000 - LT1
# Completed on:{COMPLETION DATE}


### INITIALIZATIONS ###
from game import Game
import pygame as pg
import pygame_gui as pgg
import sys
import os

pg.init()
pg.font.init()

main_font = pg.font.SysFont('Verdana', 10)
large_font = pg.font.SysFont('Verdana', 18)
x_large_font = pg.font.SysFont('Verdana', 32)


### CLASS CREATIONS ###

## Button Class for easy button and text drawing onto page ##
class Button():
    def __init__(self, x, y, w, h, text):
        self._x = x
        self._y = y
        self._h = h
        self._w = w
        self._text = text

    def draw(self, window):  # Draws rectangle of w width and h height at (x,y)
        button_image = pg.Rect(self._x, self._y, self._w, self._h)
        pg.draw.rect(window, ("dimgrey"), button_image, width=3, border_radius=5)
        display_text = main_font.render(self._text, False, color="dimgrey")  # Draws text onto button
        window.blit(display_text, (self._x + 7, self._y + 3))

    def draw_large(self, window):  # Draws rectangle of w width and h height at (x,y) with larger text
        button_image = pg.Rect(self._x, self._y, self._w, self._h)
        pg.draw.rect(window, ("dimgrey"), button_image, width=3, border_radius=5)
        display_text = large_font.render(self._text, False, color="dimgrey")  # Draws text onto button
        window.blit(display_text, (self._x + 7, self._y + 3))


### FUNCTION CREATIONS ###



### WINDOW CREATIONS ###

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

        # Wait until the music finishes playing
        while pg.mixer.music.get_busy():  # Keep playing until it's done
            pg.time.Clock().tick(10)  # Delay to avoid high CPU usage during the wait

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
        "1. Select the difficulty (K-2, 3-5, 6-8).",
        "2. Select the grid size and number of players (2-5 and up).",
        "3. Watch as players wander aimlessly through the woods.",
        "4. The goal is to reach all of your friends in the woods.",
        "5. Have fun and good luck!"
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
    str_item_list = [str(i) for i in range(5, 21)]  # Value inits
    grid_width_bool = False
    grid_height_bool = False
    player_number_bool = False

    selection_screen = pg.display.set_mode((400, 300))  # Screen inits
    pg.display.set_caption("Gameplay Selection")
    background = pg.Surface((400, 300))
    background.fill("whitesmoke")
    selection_screen.blit(background, (0, 0))
    pgmanager = pgg.UIManager((400, 300))  # Manager to check for UI selection list selections
    selection_clock = pg.time.Clock()
    refresh = selection_clock.tick(60) / 1000
    width_text = large_font.render("Grid Width", False, color="dimgrey")  # Text inits
    selection_screen.blit(width_text, (25, 75))
    height_text = large_font.render("Grid Height", False, color="dimgrey")
    selection_screen.blit(height_text, (150, 75))
    player_text = large_font.render("# of Players", False, color="dimgrey")
    selection_screen.blit(player_text, (265, 75))

    # Creates 3 UI selection lists of allowed integer values for grid width, grid height, and # of players respectively
    width_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(25, 100, 100, 125), item_list=str_item_list,
                                             manager=pgmanager, object_id="grid_width")
    height_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(150, 100, 100, 125), item_list=str_item_list,
                                              manager=pgmanager, object_id="grid_height")
    player_box = pgg.elements.UISelectionList(relative_rect=pg.Rect(275, 100, 100, 65), item_list=["2", "3", "4"],
                                              manager=pgmanager, object_id="player_number")

    continue_button = Button(275, 175, 100, 50, "Continue")  # Button init
    continue_button.draw_large(selection_screen)

    running = True

    while running:

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:  # Returns to main menu if x-ed out
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                # Continues to next selection screen if all 3 selectinos have been made, and the continue button has been pressed
                if grid_width_bool and grid_height_bool and player_number_bool and (275 <= mouse_pos[0] <= 375) and (
                        175 <= mouse_pos[1] <= 225):
                    grid_and_player_selection(int(grid_width), int(grid_height), int(player_number))

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (
                    25 <= mouse_pos[0] <= 125):  # Uses same elif statement where
                grid_width = event.text  # events of new list selection type at correct UI box location
                grid_width_bool = True  # updates appropriate variable as well as changes a bool to True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (150 <= mouse_pos[0] <= 250):
                grid_height = event.text
                grid_height_bool = True

            elif event.type == pgg.UI_SELECTION_LIST_NEW_SELECTION and (275 <= mouse_pos[0] <= 375):
                player_number = event.text
                player_number_bool = True

            pgmanager.process_events(event)  # Used for pygame GUI events

        pgmanager.update(refresh)  # Refreshes pgmanager with display update
        pgmanager.draw_ui(selection_screen)  # Draws UI selection lists
        pg.display.update()

    main_game_gui()


## Grid and Player Selection function creates a new window that takes in previously selected grid width, height, and # of players ##
## and lets the user pick where each player will be starting on the grid ##
def grid_and_player_selection(grid_width, grid_height, number_of_players):

    cell_size = 50  # Size of each grid cell
    grid_offset_x, grid_offset_y = 50, 100  # Where the grid starts
    selected_positions = {}  # Store selected positions for players

    player_colors = {  # assign colors for players
        1: (255, 0, 0),  # Player 1 - Red
        2: (0, 0, 255),  # Player 2 - Blue
        3: (0, 255, 0),  # Player 3 - Green
        4: (255, 255, 0)  # Player 4 - Yellow
    }

    selection_screen = pg.display.set_mode((375, 200 + 100 * number_of_players))  # Screen inits
    pg.display.set_caption("Gameplay Selection")
    background = pg.Surface((375, 200 + 100 * number_of_players))
    background.fill("whitesmoke")
    selection_screen.blit(background, (0, 0))
    pgmanager = pgg.UIManager((375, 200 + 100 * number_of_players))  # GUI manager inits
    selection_clock = pg.time.Clock()
    refresh = selection_clock.tick(60) / 1000
    matching_coords_text = large_font.render("Player coordinates cannot match!", None,
                                             color="dimgrey")  # Text init for later

    start_button = Button(250, 150 + 100 * number_of_players, 90, 40, "Start!")  # Start Button init
    start_button.draw_large(selection_screen)

    pg.init()
    selection_screen = pg.display.set_mode((grid_width * cell_size + 100, grid_height * cell_size + 150))
    pg.display.set_caption("Player Selection")

    background = pg.Surface(selection_screen.get_size())
    background.fill("whitesmoke")
    selection_screen.blit(background, (0, 0))

    pgmanager = pgg.UIManager(selection_screen.get_size())
    selection_clock = pg.time.Clock()
    refresh = selection_clock.tick(60) / 1000

    # "Start" button (disabled until all players pick a position)
    start_button = Button(selection_screen.get_width() // 2 - 45, grid_height * cell_size + 120, 90, 40, "Start")

    current_player = 1  # Start with Player 1

    running = True
    while running:
        selection_screen.fill((240, 240, 240))
        pg.draw.rect(selection_screen, (0, 0, 0),
                     (grid_offset_x - 5, grid_offset_y - 5, grid_width * cell_size + 10, grid_height * cell_size + 10),
                     3)

        # Draw the grid
        for x in range(grid_width):
            for y in range(grid_height):
                rect = pg.Rect(grid_offset_x + x * cell_size, grid_offset_y + y * cell_size, cell_size, cell_size)
                pg.draw.rect(selection_screen, (0, 0, 0), rect, 1)

                # If selected, fill cell with player's color
                for player, pos in selected_positions.items():
                    if pos == (x, y):
                        pg.draw.rect(selection_screen, player_colors[player], rect)

        instructions = large_font.render(f"Player {current_player}, click to choose starting position", True, (0, 0, 0))
        selection_screen.blit(instructions, (50, 50))
        start_button.draw_large(selection_screen)

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                # Click grid
                for x in range(grid_width):
                    for y in range(grid_height):
                        rect = pg.Rect(grid_offset_x + x * cell_size, grid_offset_y + y * cell_size, cell_size,
                                       cell_size)
                        if rect.collidepoint(mouse_pos):
                            if (x, y) not in selected_positions.values() and (x, y) not in selected_positions.keys():
                                selected_positions[current_player] = (x, y)
                                if current_player < number_of_players:
                                    current_player += 1

                # Start game
                if len(selected_positions) == number_of_players and (
                        start_button._x <= mouse_pos[0] <= start_button._x + start_button._w
                ) and (
                        start_button._y <= mouse_pos[1] <= start_button._y + start_button._h
                ):
                    print("Game Starting with selected positions:", selected_positions)
                    player_positions = list(selected_positions.values())
                    game = Game(grid_width, grid_height, player_positions, cell_size=40)  # Ensure correct cell size
                    game.run()
            pgmanager.process_events(event)

        pgmanager.update(refresh)
        pgmanager.draw_ui(selection_screen)
        pg.display.update()

    main_game_gui()  # Runs Main Game function if x-ed out

def start_k2_game(): #k-2 level
    grid_width, grid_height = 6, 6  # Fixed grid size
    player_positions = [(0, 0), (grid_width - 1, grid_height - 1)]  # Opposite corners
    game = Game(grid_width, grid_height, player_positions, cell_size=40)
    game.run()

## Main Game GUI Function is the main function that needs to be launched for the game to begin. Users select level, or can click ##
## About to see how the game works ##
def main_game_gui():
    game_creation_screen = pg.display.set_mode((325, 500))  # Screen inits
    pg.display.set_caption("Main Menu | Wandering in the Woods")
    background = pg.Surface((325, 500))
    background.fill("whitesmoke")
    game_creation_screen.blit(background, (0, 0))
    display_text = x_large_font.render("Wandering", False, color="dimgrey")  # Text inits
    game_creation_screen.blit(display_text, (75, 360))
    display_text_2 = x_large_font.render("in the", False, color="dimgrey")
    game_creation_screen.blit(display_text_2, (115, 400))
    display_text_3 = x_large_font.render("Woods", False, color="dimgrey")
    game_creation_screen.blit(display_text_3, (107, 440))

    K_though_2_button = Button(25, 300, 75, 50, "K Through 2")  # Button inits
    K_though_2_button.draw(game_creation_screen)

    three_through_5_button = Button(125, 300, 75, 50, "3 Through 5")
    three_through_5_button.draw(game_creation_screen)

    six_through_8_button = Button(225, 300, 75, 50, "6 Through 8")
    six_through_8_button.draw(game_creation_screen)

    about_button = Button(250, 25, 50, 25, "About")
    about_button.draw(game_creation_screen)

    # RRFIX: Create picture for main menu

    running = True
    while running:

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                pg.quit()  # When the main menu is closed, pygame is quit and the program is terminated
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()

                if (25 <= mouse_pos[0] <= 100) and (300 <= mouse_pos[1] <= 350):
                    start_k2_game()  # Run K-2 game directly


                elif (125 <= mouse_pos[0] <= 200) and (300 <= mouse_pos[1] <= 350):
                    selection_window()

                elif (225 <= mouse_pos[0] <= 300) and (300 <= mouse_pos[1] <= 350):
                    selection_window()

                elif (250 <= mouse_pos[0] <= 300) and (25 <= mouse_pos[1] <= 50):
                    about_window()

        pg.display.update()
    return None


main_game_gui()
