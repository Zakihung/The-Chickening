# modules/screens/game_screen.py
import pygame

from modules.managers.item_manager import ItemManager
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.entities.player import Player
from modules.managers.level_manager import LevelManager

class GameScreen:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager  # Thêm dòng này để gán param vào instance
        self.background_color = COLOR_GREEN
        self.player = Player(self.sound_manager)
        self.level_manager = LevelManager(self.sound_manager)
        self.player.enemies = self.level_manager.enemies
        self.resources = []
        self.item_manager = ItemManager()

    def update(self, delta_time, keys):
        """Update entities với delta_time và keys."""
        for res in self.resources[:]:
            res.update(delta_time, self.player)
            if not res.alive:
                self.resources.remove(res)
        self.resources.extend(self.player.dropped_resources)
        self.player.dropped_resources.clear()
        # Test store on key T
        if keys[pygame.K_t]:
            self.player.store_thoc()

    def draw_background(self):
        """Draw background và entities."""
        self.screen.fill(self.background_color)
        self.level_manager.draw(self.screen)
        self.player.draw(self.screen)
        for res in self.resources:
            res.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))  # Grass placeholder