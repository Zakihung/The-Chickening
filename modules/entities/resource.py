# modules/entities/resource.py
import pygame
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
        self.image = None  # Load thoc.png sau
        self.alive = True  # Để collect

    def update(self, delta_time, player=None):
        """
        Update: Check collide player để collect.
        """
        if player and rect_collision(self.rect, player.rect):
            player.thoc += self.amount  # Add to player thoc (placeholder)
            self.alive = False  # Remove sau collect
            # TODO: Sound/effect

    def draw(self, screen):
        """
        Draw: Vẽ thóc (circle vàng placeholder).
        """
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.circle(screen, COLOR_YELLOW, self.rect.center, 10)