# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.entities.player import Player
from modules.entities.enemy import Enemy

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = COLOR_GREEN
        self.player = Player()
        self.test_enemy = Enemy(600, 300, 'shield')  # Type 'shield'
        self.player.enemies = [self.test_enemy]  # Giữ cho projectile hit enemy

    def update(self, delta_time, keys):
        """Update entities với delta_time và keys."""
        self.player.update(delta_time, keys)
        self.test_enemy.update(delta_time, self.player)

        # Test damage nếu không invincible (optional, có thể xóa sau)
        if not self.player.invincible:
            self.player.take_damage(0.1)  # Test HP giảm chậm

    def draw_background(self):
        """Draw background và entities."""
        self.screen.fill(self.background_color)
        self.player.draw(self.screen)
        self.test_enemy.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))  # Grass placeholder