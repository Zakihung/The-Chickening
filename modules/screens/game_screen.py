# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = COLOR_GREEN
        # Load sprite test
        self.chicken_sprite = pygame.image.load('assets/images/player/chicken.png')  # Đường dẫn tương đối từ root
        self.chicken_rect = self.chicken_sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Vị trí giữa màn
        self.chicken_sprite = pygame.transform.scale(self.chicken_sprite, (300, 300)) # scale gà nhỏ lại

    def draw_background(self):
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

    def draw_test_sprite(self):
        """Hàm vẽ sprite test (gà con)."""
        self.screen.blit(self.chicken_sprite, self.chicken_rect)