import pygame as pg
import random

class Player:  # Player position
    def __init__(self, player_id, x, y, grid_size, color, stats, cell_size=40):  # Include stats tracker
        self.player_id = player_id
        self.x = x
        self.y = y
        self.grid_size = grid_size  # (cols, rows)
        self.color = color # Assigned color
        self.cell_size = cell_size  # dynamic cell size
        self.rect = pg.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

        self.group = [self]

    def move(self):
        if len(self.group) > 1:
            # Group moves as a unit
            leader = self.group[0]  # The first player in the group is the leader
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Random movements in all 4 directions
            dx, dy = random.choice(directions)
            new_x, new_y = leader.x + dx, leader.y + dy

            if 0 <= new_x < self.grid_size[0] and 0 <= new_y < self.grid_size[1]:
                for p in self.group:
                    p.x, p.y = new_x, new_y
        else:
            # Move individually
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            dx, dy = random.choice(directions)
            new_x, new_y = self.x + dx, self.y + dy

            if 0 <= new_x < self.grid_size[0] and 0 <= new_y < self.grid_size[1]:
                self.x, self.y = new_x, new_y

        self.update_position()

    def update_position(self): # updates player rectangle position
        self.rect.topleft = (self.x * self.cell_size, self.y * self.cell_size)

    def draw(self, screen): # draws the player on the grid
        pg.draw.rect(screen, self.color, self.rect)
