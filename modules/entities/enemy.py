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
        self.zigzag_amplitude = 50  # Biên độ lắc zig-zag (pixels)
        self.zigzag_frequency = 5  # Tần số lắc (cao hơn = nhanh lắc)
        self.time = 0  # Timer cho sin wave
        self.attack_damage = 10  # Damage cào vuốt khi áp sát
        self.attack_range = 50  # Range để attack (placeholder)

    def update(self, delta_time, player=None):
        """
        Override update: AI simple - di chuyển ngẫu nhiên, hoặc zig-zag áp sát nếu 'runner'.
        :param player: Player instance để target
        """
        super().update(delta_time)

        self.time += delta_time  # Update time cho sin

        if player:
            # Tính direction tới player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                base_dir = pygame.Vector2(dx / dist, dy / dist)  # Normalize to player

                if self.type == 'runner':
                    # Zig-zag AI: Thêm offset sin cho y (lắc lên xuống)
                    offset = math.sin(
                        self.time * self.zigzag_frequency) * self.zigzag_amplitude / dist  # Scale với dist
                    self.direction = pygame.Vector2(base_dir.x, base_dir.y + offset)
                    self.direction.normalize_ip() if self.direction.length() > 0 else None
                    self.speed = ENEMY_SPEED_BASE * 1.5  # Tốc độ nhanh hơn cho runner

                    # Attack nếu trong range (placeholder damage)
                    if dist < self.attack_range and not player.invincible:
                        player.take_damage(self.attack_damage)
                        # Cooldown attack sau

                else:
                    # Fallback random nếu không phải runner
                    self.direction_change_timer -= delta_time
                    if self.direction_change_timer <= 0:
                        angle = random.uniform(0, 2 * math.pi)
                        self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                        self.direction_change_timer = random.uniform(1, 2)
        else:
            # No player: Random AI
            self.direction_change_timer -= delta_time
            if self.direction_change_timer <= 0:
                angle = random.uniform(0, 2 * math.pi)
                self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                self.direction_change_timer = random.uniform(1, 2)

        # Check collision với player (apply damage nếu chạm)
        if player and rect_collision(self.rect, player.rect) and not player.invincible:
            player.take_damage(10)  # Damage placeholder khi chạm

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