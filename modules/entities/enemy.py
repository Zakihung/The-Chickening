# modules/entities/enemy.py
import math
import pygame
import random
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    ENEMY_HP_BASE, ENEMY_SPEED_BASE, COLOR_RED, DROP_THO_RATE, SCREEN_WIDTH, SCREEN_HEIGHT
)
from modules.utils.helpers import rect_collision  # Để collision sau

class Enemy(BaseEntity):
    def __init__(self, x, y, enemy_type='runner'):
        """
        Class base cho kẻ thù: Cáo đỏ.
        :param x, y: Vị trí spawn
        :param enemy_type: 'runner', 'archer', etc. để override behavior sau
        """
        width, height = 50, 50  # Kích thước placeholder
        super().__init__(x, y, width, height, hp=ENEMY_HP_BASE, speed=ENEMY_SPEED_BASE)
        self.type = enemy_type
        self.image = None  # Load sprite sau (fox.png)
        # Placeholder image: Rect đỏ
        try:
            # self.image = pygame.image.load('assets/images/enemies/fox.png')
            # self.image = pygame.transform.scale(self.image, (50, 50))
            pass
        except pygame.error:
            pass

        # AI attributes
        self.direction_change_timer = random.uniform(1, 2)  # Change direction sau 1-2s
        self.target = None  # Placeholder cho player target (áp sát sau)

    def update(self, delta_time, player=None):
        """
        Override update: AI simple - di chuyển ngẫu nhiên, change direction random.
        :param player: Player instance để target sau (áp sát)
        """
        super().update(delta_time)

        # Random movement AI
        self.direction_change_timer -= delta_time
        if self.direction_change_timer <= 0:
            # Change to random direction
            angle = random.uniform(0, 2 * math.pi)
            self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            self.direction_change_timer = random.uniform(1, 2)  # Reset timer

        # Placeholder cho type-specific AI (override trong subclass)
        if self.type == 'runner':
            # Sau này: Áp sát player zig-zag
            pass

        # Check collision với player (apply damage nếu chạm)
        if player and rect_collision(self.rect, player.rect) and not player.invincible:
            player.take_damage(10)  # Damage placeholder khi chạm
            # Bounce back hoặc logic khác

        # Drop thóc khi chết (placeholder print)
        if not self.alive:
            if random.random() < DROP_THO_RATE:
                print("Dropped thóc!")  # TODO: Tạo resource.py drop

    def draw(self, screen):
        """
        Override draw: Vẽ enemy với color theo type (placeholder).
        """
        color = COLOR_RED  # Default đỏ cho cáo
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, color, self.rect)
        super().draw(screen)  # HP bar