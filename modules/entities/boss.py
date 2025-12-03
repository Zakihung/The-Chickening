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
        self.projectiles = []  # List projectiles (spear)
        self.attack_cooldown = 0  # Cooldown attacks
        self.dash_duration = 0  # Thời gian dash temp
        self.dash_multiplier = 2.0  # Tăng speed x2 khi dash
        self.spear_damage = 40  # Sát thương thương
        self.spear_speed = 12  # Tốc độ spear proj
        self.spear_length = 100  # Range dài
        self.charge_cooldown_base = 3.0  # Cooldown base
        self.rage_mult = 1.5  # Tăng phase 3

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
        elif hp_ratio < self.phase_thresholds[1] and self.phase < 3:
            self.phase = 3
            self.speed *= 1.2  # Thêm tốc
            self.summon_minions(5)  # Summon cáo con

        if player and self.attack_cooldown <= 0:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                base_dir = pygame.Vector2(dx / dist, dy / dist)
                self.direction = base_dir

                if self.phase == 1:
                    # Phase 1: Base charge + spear
                    self.dash_duration = 1.0
                    spear = Projectile(self.rect.centerx, self.rect.centery, base_dir, 'ranged', self.spear_damage, self.spear_speed, length=self.spear_length)
                    self.projectiles.append(spear)
                    self.attack_cooldown = self.charge_cooldown_base

                elif self.phase == 2:
                    # Phase 2: Frequent charge, double spear
                    self.dash_duration = 1.5
                    for i in [-0.1, 0.1]:
                        offset_dir = base_dir.rotate(i * 30)
                        spear = Projectile(self.rect.centerx, self.rect.centery, offset_dir, 'ranged', self.spear_damage, self.spear_speed, length=self.spear_length)
                        self.projectiles.append(spear)
                    self.attack_cooldown = self.charge_cooldown_base * 0.7

                elif self.phase == 3:
                    # Phase 3: Rage, summon on charge
                    self.dash_duration = 2.0
                    self.spear_damage *= self.rage_mult
                    spear = Projectile(self.rect.centerx, self.rect.centery, base_dir, 'ranged', self.spear_damage, self.spear_speed * self.rage_mult, length=self.spear_length * 1.5)
                    self.projectiles.append(spear)
                    self.summon_minions(2)
                    self.attack_cooldown = self.charge_cooldown_base * 0.5

        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        # Dash logic
        if self.dash_duration > 0:
            self.dash_duration -= delta_time
            self.speed *= self.dash_multiplier
            if self.dash_duration <= 0:
                self.speed /= self.dash_multiplier

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update(delta_time)
            proj.check_collision([player])
            if not proj.alive:
                self.projectiles.remove(proj)

        # Update minions
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
        """Override draw: Vẽ boss lớn, minions, projectiles."""
        super().draw(screen)
        # Vẽ minions
        for minion in self.minions:
            minion.draw(screen)
        # Vẽ projectiles
        for proj in self.projectiles:
            proj.draw(screen)