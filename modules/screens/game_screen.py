# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.utils.helpers import rect_collision
import json
from modules.utils.constants import ASSETS_PATH  # Nếu cần, nhưng chưa dùng
from modules.entities.base_entity import BaseEntity
from modules.entities.player import Player
from modules.entities.enemy import Enemy

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = COLOR_GREEN
        # Load sprite test
        self.chicken_sprite = pygame.image.load('assets/images/player/chicken.png')  # Đường dẫn tương đối từ root
        self.chicken_rect = self.chicken_sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Vị trí giữa màn
        self.player = Player()
        self.test_enemy = BaseEntity(600, 300, 50, 50, hp=50, speed=0)  # Enemy tĩnh để test hit
        self.test_enemy = Enemy(600, 300, 'runner')  # Type 'runner' để test zig-zag
        self.player.enemies = [self.test_enemy]  # Giữ cho projectile hit

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
        # Lấy keys cho input
        keys = pygame.key.get_pressed()
        # Update và draw player
        delta_time = 1 / 60  # Giả, sau dùng thực từ clock
        self.player.update(delta_time, keys)
        self.player.draw(self.screen)
        self.player.take_damage(0.1)  # Test giảm HP chậm để thấy bar

        keys = pygame.key.get_pressed()
        self.player.update(delta_time, keys)
        self.player.draw(self.screen)
        self.test_enemy.update(delta_time, self.player)
        self.test_enemy.draw(self.screen)
        # Test damage chỉ nếu không invincible
        if not self.player.invincible:
            self.player.take_damage(0.1)  # Test HP giảm chậm, nhưng skip khi dodge
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