# modules/entities/base_entity.py
import pygame
from modules.utils.constants import PLAYER_HP_DEFAULT, ENEMY_HP_BASE
from modules.utils.helpers import rect_collision  # Để dùng sau cho collision

class BaseEntity:
    def __init__(self, x, y, width, height, hp=None, speed=0):
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

    def update(self, delta_time):
        """
        Update logic mỗi frame (di chuyển, check chết, etc.).
        Override trong subclass.
        :param delta_time: Thời gian giữa frames (cho movement mượt)
        """
        if self.hp <= 0:
            self.alive = False

    def draw(self, screen):
        """
        Vẽ entity lên screen.
        Override để vẽ sprite thực.
        """
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            # Placeholder: Vẽ rect đỏ cho test
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def take_damage(self, damage):
        """
        Giảm HP khi trúng đòn.
        :param damage: Sát thương nhận
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_colliding_with(self, other_entity):
        """
        Check collision với entity khác.
        """
        return rect_collision(self.rect, other_entity.rect)