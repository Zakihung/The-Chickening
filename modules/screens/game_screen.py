# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.entities.player import Player
from modules.entities.enemy import Enemy
from modules.entities.boss import Boss
from modules.managers.level_manager import LevelManager

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = COLOR_GREEN
        self.player = Player()
        self.test_boss = Boss(600, 300, 'boss1')
        self.player.enemies = [self.test_boss]  # Để hit boss
        self.resources = []  # List Resource
        self.level_manager = LevelManager()

    def update(self, delta_time, keys):
        """Update entities với delta_time và keys."""
        self.player.update(delta_time, keys)
        self.test_boss.update(delta_time, self.player)
        self.level_manager.update(delta_time, self.player)

        # Update resources (bao gồm dropped từ player.die)
        for res in self.resources[:]:
            res.update(delta_time, self.player)
            if not res.alive:
                self.resources.remove(res)
        # Add dropped từ player
        for drop in self.player.dropped_resources[:]:
            self.resources.append(drop)
            self.player.dropped_resources.remove(drop)

        # Test damage nếu không invincible (optional, có thể xóa sau)
        if not self.player.invincible:
            self.player.take_damage(0.1)  # Test HP giảm chậm

    def draw_background(self):
        """Draw background và entities."""
        self.screen.fill(self.background_color)
        self.player.draw(self.screen)
        self.test_boss.draw(self.screen)
        for res in self.resources:
            res.draw(self.screen)
        self.level_manager.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))  # Grass placeholder