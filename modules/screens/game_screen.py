# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.entities.player import Player
from modules.managers.level_manager import LevelManager

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = COLOR_GREEN
        self.player = Player()
        self.level_manager = LevelManager()
        self.player.enemies = self.level_manager.enemies  # Link to level enemies for collision
        self.resources = []  # List Resource

    def update(self, delta_time, keys):
        """Update entities với delta_time và keys."""
        self.player.update(delta_time, keys)
        self.level_manager.update(delta_time, self.player)

        # Update resources
        for res in self.resources[:]:
            res.update(delta_time, self.player)
            if not res.alive:
                self.resources.remove(res)
        # Add dropped from player die
        self.resources.extend(self.player.dropped_resources)
        self.player.dropped_resources.clear()

        # Test damage nếu không invincible (optional)
        if not self.player.invincible:
            self.player.take_damage(0.1)  # Test HP giảm chậm

    def draw_background(self):
        self.level_manager.draw(self.screen)  # Draw bg/obs/enemies/spawns
        self.player.draw(self.screen)
        for res in self.resources:
            res.draw(self.screen)