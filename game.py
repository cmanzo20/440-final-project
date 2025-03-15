import pygame
import sys
from grid import Grid
from player import Player
from stats import Stats

class Game:
    def __init__(self, grid_width, grid_height, player_positions, cell_size=40):
        pygame.init()
        self.grid = Grid(grid_width, grid_height, cell_size)
        self.stats = Stats()  # Initialize stats tracking
        self.stats.start_timer()  # Start the timer when the game begins
        window_width = grid_width * cell_size
        window_height = grid_height * cell_size
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

        # k-2 ends when the palyers meet
        if len(self.players) == 2 and len(self.groups) == 1:
            print("Players met!")
            if len(self.players) == 2 and len(self.groups) == 1:
                print("K-2: Players met!")

                self.stats.stop_timer()  # Stop the timer when the game ends
                self.stats.save_stats()  # Save stats before showing
                self.game_over()
                return


        # **For 3-5 and 6-8: Continue Until All Players Are Together**
        elif len(self.groups) == 1 and len(self.groups[0]) == len(self.players):
            print("All players have found each other!")

            self.stats.stop_timer()  # Stop the timer when the game ends
            self.stats.save_stats()  # Save stats before showing
            self.game_over()

            self.display_full_stats()


    def display_full_stats(self):

        self.screen.fill((255, 255, 255))  # White background
        stats_font = pygame.font.SysFont('Verdana', 16)


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

        pygame.display.flip()
        pygame.time.delay(5000)  # Display stats for 5 seconds before returning to main menu
        from Main import main_game_gui
        main_game_gui()  # Return to main menu

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
