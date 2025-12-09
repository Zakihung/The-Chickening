# modules/entities/resource.py
import pygame
import os
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import COLOR_YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT
from modules.utils.helpers import rect_collision

class Resource(BaseEntity):
    def __init__(self, x, y, amount=10):
        """
        Class cho tài nguyên: Thóc.
        :param x, y: Vị trí spawn (near enemy chết)
        :param amount: Số thóc (random 5-20)
        """
        super().__init__(x, y, 20, 20, hp=0, speed=0)  # No HP/speed
        self.amount = amount
        sprite_path = os.path.join('assets', 'images', 'resources', 'thoc.png')
        if os.path.exists(sprite_path):
            self.image = pygame.image.load(sprite_path)
            self.image = pygame.transform.scale(self.image, (300, 300))
        else:
            self.image = None
        self.alive = True  # Để collect

    def update(self, delta_time, player=None):
        """
        Update: Check collide player để collect.
        """
        if player and rect_collision(self.rect, player.rect):
            player.thoc_collected += self.amount
            self.alive = False

    def draw(self, screen):
        """
        Draw: Vẽ thóc (circle vàng placeholder).
        """
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.circle(screen, COLOR_YELLOW, self.rect.center, 10)