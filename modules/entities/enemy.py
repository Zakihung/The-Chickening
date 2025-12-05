# modules/entities/enemy.py
import math
import pygame
import random
from modules.entities.base_entity import BaseEntity
from modules.managers import item_manager
from modules.screens import game_screen
from modules.utils.constants import (
    ENEMY_HP_BASE, ENEMY_SPEED_BASE, COLOR_RED, DROP_THO_RATE, SCREEN_WIDTH, SCREEN_HEIGHT, BOMB_AOE_RADIUS
)
from modules.utils.helpers import rect_collision
from modules.entities.projectile import Projectile
from modules.entities.resource import Resource

class Enemy(BaseEntity):
    def __init__(self, x, y, enemy_type='runner', sound_manager=None):
        width, height = 50, 50  # Kích thước placeholder
        super().__init__(x, y, width, height, hp=ENEMY_HP_BASE, speed=ENEMY_SPEED_BASE)
        self.type = enemy_type
        self.image = None
        self.sound_manager = sound_manager  # Pass from game_screen
        self.direction_change_timer = random.uniform(1, 2)
        self.zigzag_amplitude = 50
        self.zigzag_frequency = 5
        self.time = 0
        self.attack_damage = 10
        self.attack_range = 50
        self.min_distance = 200
        self.max_distance = 300
        self.shoot_cooldown = 0
        self.arrow_damage = 20
        self.arrow_speed = 8
        self.projectiles = []
        self.bomb_throw_cooldown = 0
        self.bomb_damage = 30
        self.bomb_speed = 4
        self.bomb_throw_range_min = 200
        self.bomb_throw_range_max = 400
        self.shield_turn_timer = 0
        self.shield_turn_duration = 0
        self.shield_cooldown = 0
        self.back_weak_mult = 2.0
        self.front_resist_mult = 0.2
        self.shield_hp = 50
        self.shield_max_hp = 50
        self.facing_player = True
        self.fire_cast_cooldown = 0
        self.buff_cooldown = 0
        self.barrier_cooldown = 0
        self.fire_damage = 25
        self.fire_speed = 7
        self.buff_amount = 1.5
        self.buff_duration = 0
        self.barrier_radius = 80
        self.barrier_projectiles = []
        self.allies = []
        self.dropped = False
        self.stun_timer = 0

    def update(self, delta_time, player=None):
        super().update(delta_time)

        if self.stun_timer > 0:
            self.stun_timer -= delta_time
            self.direction = pygame.Vector2(0, 0)
            return

        self.time += delta_time

        if player:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                base_dir = pygame.Vector2(dx / dist, dy / dist)

                if self.type == 'runner':
                    offset = math.sin(self.time * self.zigzag_frequency) * self.zigzag_amplitude / dist
                    self.direction = pygame.Vector2(base_dir.x, base_dir.y + offset)
                    if self.direction.length() > 0:
                        self.direction.normalize_ip()
                    self.speed = ENEMY_SPEED_BASE * 1.5

                    if dist < self.attack_range and not player.invincible:
                        player.take_damage(self.attack_damage)

                elif self.type == 'archer':
                    if dist < self.min_distance:
                        self.direction = -base_dir
                    elif dist > self.max_distance:
                        self.direction = base_dir
                    else:
                        self.direction = pygame.Vector2(0, 0)
                        if self.shoot_cooldown <= 0:
                            arrow_dir = base_dir
                            arrow = Projectile(self.rect.centerx, self.rect.centery, arrow_dir, 'ranged', self.arrow_damage, self.arrow_speed)
                            self.projectiles.append(arrow)
                            self.shoot_cooldown = 1.5

                    if self.shoot_cooldown > 0:
                        self.shoot_cooldown -= delta_time

                    for proj in self.projectiles[:]:
                        proj.update(delta_time)
                        proj.check_collision([player])
                        if not proj.alive:
                            self.projectiles.remove(proj)

                elif self.type == 'bomber':
                    if dist > self.bomb_throw_range_max:
                        self.direction = base_dir
                    elif dist < self.bomb_throw_range_min:
                        self.direction = -base_dir * 0.5
                    else:
                        self.direction = pygame.Vector2(0, 0)
                        if self.bomb_throw_cooldown <= 0:
                            bomb_dir = base_dir
                            bomb = Projectile(self.rect.centerx, self.rect.centery, bomb_dir, 'bomb', self.bomb_damage, self.bomb_speed, BOMB_AOE_RADIUS)
                            self.projectiles.append(bomb)
                            self.bomb_throw_cooldown = 2.5

                    if self.bomb_throw_cooldown > 0:
                        self.bomb_throw_cooldown -= delta_time

                    for proj in self.projectiles[:]:
                        proj.update(delta_time)
                        proj.check_collision([player])
                        if not proj.alive:
                            self.projectiles.remove(proj)

                elif self.type == 'shield':
                    if dist > 0:
                        base_dir = pygame.Vector2(dx / dist, dy / dist)
                        self.direction = -base_dir  # Quay mặt player

                    if self.shield_turn_duration <= 0 and self.shield_cooldown <= 0:
                        if random.random() < 0.01:
                            self.facing_player = False
                            self.shield_turn_duration = random.uniform(1, 2)
                    if self.shield_turn_duration > 0:
                        self.shield_turn_duration -= delta_time
                        if self.shield_turn_duration <= 0:
                            self.shield_cooldown = 3.0
                            self.facing_player = True
                    if self.shield_cooldown > 0:
                        self.shield_cooldown -= delta_time

                    if dist < self.attack_range and not self.facing_player and not player.invincible:
                        player.take_damage(self.attack_damage * 1.5)

                    self.speed = ENEMY_SPEED_BASE * 0.8

                elif self.type == 'mage':
                    if dist > 0:
                        base_dir = pygame.Vector2(dx / dist, dy / dist)
                        self.direction = base_dir * 0.5

                    self.speed = ENEMY_SPEED_BASE * 0.6

                    if self.fire_cast_cooldown <= 0:
                        fire = Projectile(self.rect.centerx, self.rect.centery, base_dir, 'ranged', self.fire_damage, self.fire_speed)
                        self.projectiles.append(fire)
                        self.fire_cast_cooldown = 2.0

                    if self.buff_duration > 0:
                        self.speed *= self.buff_amount
                        self.buff_duration -= delta_time
                    if self.buff_cooldown <= 0:
                        self.buff_duration = 5.0
                        self.buff_cooldown = 10.0

                    if self.barrier_cooldown <= 0:
                        for i in range(8):
                            angle = (i / 8) * 2 * math.pi
                            barrier_dir = pygame.Vector2(math.cos(angle), math.sin(angle))
                            barrier_pos = self.rect.center + barrier_dir * self.barrier_radius
                            barrier = Projectile(barrier_pos[0], barrier_pos[1], pygame.Vector2(0,0), 'ranged', 15, 0)
                            barrier.aoe_radius = 20
                            self.barrier_projectiles.append(barrier)
                        self.barrier_cooldown = 8.0

                    for barrier in self.barrier_projectiles[:]:
                        barrier.update(delta_time)
                        barrier.check_collision([player])
                        if not barrier.alive:
                            self.barrier_projectiles.remove(barrier)

                    self.fire_cast_cooldown = max(0, self.fire_cast_cooldown - delta_time)
                    self.buff_cooldown = max(0, self.buff_cooldown - delta_time)
                    self.barrier_cooldown = max(0, self.barrier_cooldown - delta_time)

                    for proj in self.projectiles[:]:
                        proj.update(delta_time)
                        proj.check_collision([player])
                        if not proj.alive:
                            self.projectiles.remove(proj)

                else:
                    self.direction_change_timer -= delta_time
                    if self.direction_change_timer <= 0:
                        angle = random.uniform(0, 2 * math.pi)
                        self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                        self.direction_change_timer = random.uniform(1, 2)

        else:
            self.direction_change_timer -= delta_time
            if self.direction_change_timer <= 0:
                angle = random.uniform(0, 2 * math.pi)
                self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                self.direction_change_timer = random.uniform(1, 2)

        if player and rect_collision(self.rect, player.rect) and not player.invincible:
            player.take_damage(10)

        if not self.alive and not self.dropped:
            self.dropped = True
            if random.random() < DROP_THO_RATE:
                thoc = Resource(self.rect.centerx, self.rect.centery, random.randint(5, 20))
                # Add to global resources
            if random.random() < 0.2:
                item_id = game_screen.item_manager.get_random_item()  # Pass game_screen? Or global
                player.inventory.append(item_id)  # Add to inventory

    def is_back_hit(self, attacker_pos):
        to_attacker = pygame.Vector2(attacker_pos[0] - self.rect.centerx, attacker_pos[1] - self.rect.centery)
        to_attacker.normalize_ip()
        facing_dir = -self.direction if self.facing_player else self.direction
        dot = to_attacker.dot(facing_dir)
        return dot < 0

    def draw(self, screen):
        color = COLOR_RED
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, color, self.rect)
        super().draw(screen)

        for proj in self.projectiles:
            proj.draw(screen)

        for barrier in self.barrier_projectiles:
            barrier.draw(screen)