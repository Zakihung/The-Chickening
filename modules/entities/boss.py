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

        # Boss1 AI: Lao thương (charge) về player
        if player and self.attack_cooldown <= 0:
            # Tính dir tới player, charge (tăng speed temp)
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                base_dir = pygame.Vector2(dx / dist, dy / dist)
                self.direction = base_dir
                self.attack_cooldown = 3.0  # Cooldown 3s
                # Spawn 'spear' proj hoặc damage on path (placeholder melee range tăng)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

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