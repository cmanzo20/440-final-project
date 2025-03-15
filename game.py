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

