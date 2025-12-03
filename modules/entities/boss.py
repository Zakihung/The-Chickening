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
    def __init__(self, x, y, boss_type='boss1', sound_manager=None):
        super().__init__(x, y, enemy_type=boss_type, sound_manager=sound_manager)
        self.hp = ENEMY_HP_BASE * 10
        self.max_hp = self.hp
        self.speed = 3
        self.rect.inflate_ip(50, 50)
        self.phase = 1
        self.phase_thresholds = [0.5, 0.2]
        self.minions = []
        self.projectiles = []
        self.attack_cooldown = 0
        self.dash_duration = 0
        self.dash_multiplier = 2.0
        self.spear_damage = 40
        self.spear_speed = 12
        self.spear_length = 100
        self.charge_cooldown_base = 3.0
        self.rage_mult = 1.5

    def update(self, delta_time, player=None):
        super().update(delta_time, player)

        hp_ratio = self.hp / self.max_hp
        if hp_ratio < self.phase_thresholds[0] and self.phase < 2:
            self.phase = 2
            self.speed *= 1.5
        elif hp_ratio < self.phase_thresholds[1] and self.phase < 3:
            self.phase = 3
            self.speed *= 1.2
            self.summon_minions(5)

        if player and self.attack_cooldown <= 0:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                base_dir = pygame.Vector2(dx / dist, dy / dist)
                self.direction = base_dir

                if self.phase == 1:
                    self.dash_duration = 1.0
                    spear = Projectile(self.rect.centerx, self.rect.centery, base_dir, 'ranged', self.spear_damage, self.spear_speed, length=self.spear_length, sound_manager=self.sound_manager)
                    self.projectiles.append(spear)
                    self.attack_cooldown = self.charge_cooldown_base
                    if self.sound_manager:
                        self.sound_manager.play_sfx('cluck', 0.8)  # Placeholder charge sound

                elif self.phase == 2:
                    self.dash_duration = 1.5
                    for i in [-0.1, 0.1]:
                        offset_dir = base_dir.rotate(i * 30)
                        spear = Projectile(self.rect.centerx, self.rect.centery, offset_dir, 'ranged', self.spear_damage, self.spear_speed, length=self.spear_length, sound_manager=self.sound_manager)
                        self.projectiles.append(spear)
                    self.attack_cooldown = self.charge_cooldown_base * 0.7

                elif self.phase == 3:
                    self.dash_duration = 2.0
                    self.spear_damage *= self.rage_mult
                    spear = Projectile(self.rect.centerx, self.rect.centery, base_dir, 'ranged', self.spear_damage, self.spear_speed * self.rage_mult, length=self.spear_length * 1.5, sound_manager=self.sound_manager)
                    self.projectiles.append(spear)
                    self.summon_minions(2)
                    self.attack_cooldown = self.charge_cooldown_base * 0.5

        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

        if self.dash_duration > 0:
            self.dash_duration -= delta_time
            self.speed *= self.dash_multiplier
            if self.dash_duration <= 0:
                self.speed /= self.dash_multiplier

        for proj in self.projectiles[:]:
            proj.update(delta_time)
            proj.check_collision([player])
            if not proj.alive:
                self.projectiles.remove(proj)

        for minion in self.minions[:]:
            minion.update(delta_time, player)
            if not minion.alive:
                self.minions.remove(minion)

    def summon_minions(self, count):
        for _ in range(count):
            minion_x = self.rect.x + random.randint(-50, 50)
            minion_y = self.rect.y + random.randint(-50, 50)
            minion = Enemy(minion_x, minion_y, 'runner', self.sound_manager)
            minion.hp /= 2
            self.minions.append(minion)

    def draw(self, screen):
        super().draw(screen)
        for minion in self.minions:
            minion.draw(screen)
        for proj in self.projectiles:
            proj.draw(screen)