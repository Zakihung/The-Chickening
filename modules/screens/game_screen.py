# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.utils.helpers import rect_collision
import json
from modules.utils.constants import ASSETS_PATH  # Nếu cần, nhưng chưa dùng

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
        with open('data/items.json', 'r', encoding='utf-8') as f:
            items_data = json.load(f)
            print(items_data['items'][0])  # In item đầu tiên để test

        with open('data/skills.json', 'r', encoding='utf-8') as f:
            skills_data = json.load(f)
            print(skills_data['branches']['melee']['skills'][0])  # Test skill
        with open('data/levels.json', 'r', encoding='utf-8') as f:
            levels_data = json.load(f)
            print(levels_data['levels'][0])  # In level đầu tiên để test
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

    def draw_test_sprite(self):
        """Hàm vẽ sprite test (gà con)."""
        self.screen.blit(self.chicken_sprite, self.chicken_rect)

    def draw_test_collision(self, mouse_pos):
        """Test collision: Vẽ rect theo mouse, check va chạm với chicken."""
        test_rect = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, 50)  # Rect 50x50 quanh mouse
        if rect_collision(test_rect, self.chicken_rect):
            color = (255, 0, 0)  # Đỏ nếu collide
        else:
            color = (255, 255, 255)  # Trắng nếu không
        pygame.draw.rect(self.screen, color, test_rect, 3)  # Vẽ viền dày 3px