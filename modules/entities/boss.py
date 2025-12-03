# modules/entities/boss.py
import math

import pygame
import random
from modules.entities.enemy import Enemy
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_RED, ENEMY_HP_BASE
)
from modules.entities.projectile import Projectile

class Boss(Enemy):
    def __init__(self, x, y, boss_type='boss1'):
        """
        Class cho Boss: Cáo Đỏ lớn.
        Kế thừa Enemy, HP cao, size lớn, phases.
        :param boss_type: 'boss1' cho Cáo Đại Tướng
        """
        super().__init__(x, y, enemy_type=boss_type)
        self.hp = ENEMY_HP_BASE * 10  # HP cao (500)
        self.max_hp = self.hp
        self.speed = 3  # Chậm ban đầu
        self.rect.inflate_ip(50, 50)  # Size lớn hơn enemy (100x100)
        self.phase = 1  # Phase 1 base
        self.phase_thresholds = [0.5, 0.2]  # Change tại 50%, 20% HP
        self.minions = []  # List minions summon
        self.attack_cooldown = 0  # Cooldown attacks
        self.dash_duration = 0  # Thời gian dash temp
        self.dash_multiplier = 2.0  # Tăng speed x2 khi dash
        self.spear_damage = 40  # Sát thương thương
        self.spear_speed = 12  # Tốc độ spear proj
        self.spear_length = 100  # Range dài (extend hitbox hoặc proj size)

    def update(self, delta_time, player=None):
        """
        Override update: Check phases, type-specific AI.
        """
        super().update(delta_time, player)

        # Check phase transition
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < self.phase_thresholds[0] and self.phase < 2:
            self.phase = 2
            self.speed *= 1.5  # Tăng tốc phase 2
            # New skill placeholder
        elif hp_ratio < self.phase_thresholds[1] and self.phase < 3:
            self.phase = 3
            self.speed *= 1.2  # Thêm tốc
            self.summon_minions(5)  # Summon cáo con

        if player and self.attack_cooldown <= 0 and self.phase == 1:
            # Phase 1: Lao với thương
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                base_dir = pygame.Vector2(dx / dist, dy / dist)
                self.direction = base_dir
                self.dash_duration = 1.0  # Dash 1s
                self.attack_cooldown = 3.0  # Cooldown 3s
                # Spawn spear proj dài hướng player
                spear_rect = pygame.Rect(self.rect.centerx, self.rect.centery, self.spear_length, 10)
                spear = Projectile(self.rect.centerx, self.rect.centery, base_dir, 'ranged', self.spear_damage,
                                   self.spear_speed)
                spear.rect = spear_rect  # Extend rect cho long spear
                self.projectiles.append(spear)  # Reuse projectiles list từ Enemy

        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        # Dash logic
        if self.dash_duration > 0:
            self.dash_duration -= delta_time
            self.speed *= self.dash_multiplier
            if self.dash_duration <= 0:
                self.speed /= self.dash_multiplier  # Reset speed

        # Update minions (như projectiles)
        for minion in self.minions[:]:
            minion.update(delta_time, player)
            if not minion.alive:
                self.minions.remove(minion)

    def summon_minions(self, count):
        """Summon cáo con (Enemy 'runner')."""
        for _ in range(count):
            minion_x = self.rect.x + random.randint(-50, 50)
            minion_y = self.rect.y + random.randint(-50, 50)
            minion = Enemy(minion_x, minion_y, 'runner')
            minion.hp /= 2  # Minion yếu hơn
            self.minions.append(minion)

    def draw(self, screen):
        """Override draw: Vẽ boss lớn, minions."""
        super().draw(screen)
        # Vẽ minions
        for minion in self.minions:
            minion.draw(screen)