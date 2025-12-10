# modules/entities/base_entity.py
import pygame
from modules.utils.constants import PLAYER_HP_DEFAULT, ENEMY_HP_BASE, COLOR_RED, COLOR_GREEN, COLOR_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from modules.utils.helpers import rect_collision  # Để dùng sau cho collision

class BaseEntity:
    def __init__(self, x, y, width, height, hp=None, speed=0, game_screen=None):
        """
        Class base cho tất cả entities.
        :param x: Vị trí x ban đầu
        :param y: Vị trí y ban đầu
        :param width: Chiều rộng rect
        :param height: Chiều cao rect
        :param hp: HP ban đầu (default từ constants tùy type)
        :param speed: Tốc độ di chuyển (pixels/frame)
        """
        self.rect = pygame.Rect(x, y, width, height)  # Rect cho position và collision
        self.hp = hp if hp is not None else PLAYER_HP_DEFAULT  # Default cho player, override cho enemy
        self.max_hp = self.hp  # Để tính % HP sau
        self.speed = speed
        self.alive = True  # Flag để check chết chưa
        self.image = None  # Placeholder cho sprite (load sau)
        self.direction = pygame.Vector2(0, 0)  # Vector hướng di chuyển (normalize sau)
        self.game_screen = game_screen  # Pass to add popup

    def update(self, delta_time):
        """
        Update logic mỗi frame (di chuyển, check chết, etc.).
        Override trong subclass cho AI hoặc input.
        :param delta_time: Thời gian giữa frames (cho movement independent FPS)
        """
        # Di chuyển theo direction * speed * delta_time (frame independent)
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time

        # Giới hạn trong màn hình (placeholder, tùy entity)
        self.rect.clamp_ip(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Check chết
        if self.hp <= 0:
            self.alive = False

    def draw(self, screen):
        """
        Vẽ entity lên screen.
        Override để customize sprite.
        """
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            # Placeholder: Vẽ rect đỏ cho test
            pygame.draw.rect(screen, COLOR_RED, self.rect, 2)

        # Vẽ HP bar nếu alive
        if self.alive and self.max_hp > 0:
            hp_ratio = self.hp / self.max_hp
            bar_width = self.rect.width * hp_ratio
            hp_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_width, 5)  # Thanh máu trên đầu
            pygame.draw.rect(screen, COLOR_GREEN, hp_bar_rect)  # Xanh cho HP còn
            # Viền bar
            full_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
            pygame.draw.rect(screen, COLOR_BLACK, full_bar_rect, 1)

    def take_damage(self, damage, attacker_pos=None):
        """
        Giảm HP khi trúng đòn. Support attacker_pos cho directional damage (e.g., shield).
        :param damage: Sát thương nhận
        :param attacker_pos: Vị trí attacker (tuple x,y), optional
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        # Damage popup
        if self.game_screen:
            self.game_screen.popups.append({'text': str(int(damage)), 'pos': self.rect.center, 'timer': 1.0, 'color': COLOR_RED})

    def is_colliding_with(self, other_entity):
        """
        Check collision với entity khác.
        """
        return rect_collision(self.rect, other_entity.rect)