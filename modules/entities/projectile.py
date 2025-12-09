# modules/entities/projectile.py
import pygame
import math
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, BOMB_AOE_RADIUS, BOMB_DAMAGE
)
from modules.utils.helpers import rect_collision

class Projectile(BaseEntity):
    def __init__(self, x, y, direction, proj_type='ranged', damage=15, speed=10, aoe_radius=0, length=10, sound_manager=None):
        width = length if proj_type == 'ranged' else 50
        height = 10 if proj_type == 'ranged' else 50
        super().__init__(x, y, width, height, hp=1, speed=speed)
        self.direction = direction.normalize() if direction.length() > 0 else pygame.Vector2(1, 0)
        self.type = proj_type
        self.damage = damage
        self.aoe_radius = aoe_radius
        self.explode_timer = 2.0 if proj_type == 'bomb' else 0
        self.exploded = False
        self.image = None
        self.sound_manager = sound_manager

    def update(self, delta_time):
        if not self.alive:
            return

        super().update(delta_time)

        if self.type == 'bomb':
            self.explode_timer -= delta_time
            if self.explode_timer <= 0 and not self.exploded:
                self.exploded = True
                self.alive = False
                if self.sound_manager:
                    self.sound_manager.play_sfx('explosion')

        if not (0 < self.rect.centerx < SCREEN_WIDTH and 0 < self.rect.centery < SCREEN_HEIGHT):
            self.alive = False

    def draw(self, screen):
        super().draw(screen)

        color = COLOR_YELLOW if self.type == 'ranged' else (255, 100, 0)
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.circle(screen, color, self.rect.center, self.rect.width // 2)

        if self.exploded:
            pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.aoe_radius, 3)

    def check_collision(self, entities):
        hit_entities = []
        for entity in entities:
            if self.alive and entity.alive and entity != self:
                if self.type == 'ranged':
                    if rect_collision(self.rect, entity.rect):
                        entity.take_damage(self.damage, self.rect.center)
                        self.alive = False
                        hit_entities.append(entity)
                elif self.type == 'bomb' and self.exploded:
                    dist = math.hypot(self.rect.centerx - entity.rect.centerx, self.rect.centery - entity.rect.centery)
                    if dist <= self.aoe_radius:
                        entity.take_damage(self.damage, self.rect.center)
                        hit_entities.append(entity)
        return hit_entities