# modules/entities/enemy.py
import math
import pygame
import random
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    ENEMY_HP_BASE, ENEMY_SPEED_BASE, COLOR_RED, DROP_THO_RATE, BOMB_AOE_RADIUS
)
from modules.utils.helpers import rect_collision  # Để collision sau
from modules.entities.projectile import Projectile  # Để spawn arrow

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
        self.min_distance = 200  # Khoảng cách min để né (né nếu player < min)
        self.max_distance = 300  # Khoảng cách max để bắn (bắn nếu dist <= max)
        self.shoot_cooldown = 0  # Cooldown bắn tên (seconds, ví dụ 1.5s)
        self.arrow_damage = 20  # Sát thương tên
        self.arrow_speed = 8  # Tốc độ tên
        self.projectiles = []  # List Projectile cho arrows của enemy (tương tự player)
        self.bomb_throw_cooldown = 0  # Cooldown ném bom (seconds, ví dụ 2.5s)
        self.bomb_damage = 30  # Sát thương bom (cao hơn arrow)
        self.bomb_speed = 4  # Tốc độ ném bom (chậm hơn arrow)
        self.bomb_throw_range_min = 200  # Min dist để ném
        self.bomb_throw_range_max = 400  # Max dist để ném

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
                    if self.direction.length() > 0:
                        self.direction.normalize_ip()
                    self.speed = ENEMY_SPEED_BASE * 1.5  # Tốc độ nhanh hơn cho runner

                    # Attack nếu trong range (placeholder damage)
                    if dist < self.attack_range and not player.invincible:
                        player.take_damage(self.attack_damage)
                        # Cooldown attack sau

                elif self.type == 'archer':
                    # Archer AI: Giữ khoảng cách, né nếu gần, bắn nếu trong range
                    if dist < self.min_distance:
                        # Né: Di chuyển ngược direction tới player
                        self.direction = -base_dir
                    elif dist > self.max_distance:
                        # Áp sát nhẹ để vào range bắn
                        self.direction = base_dir
                    else:
                        # Giữ vị trí, bắn
                        self.direction = pygame.Vector2(0, 0)  # Dừng di chuyển
                        if self.shoot_cooldown <= 0:
                            # Spawn arrow hướng tới player
                            arrow_dir = base_dir
                            arrow = Projectile(self.rect.centerx, self.rect.centery, arrow_dir, 'ranged',
                                               self.arrow_damage, self.arrow_speed)
                            self.projectiles.append(arrow)
                            self.shoot_cooldown = 1.5  # Reset cooldown

                    # Update cooldown
                    if self.shoot_cooldown > 0:
                        self.shoot_cooldown -= delta_time

                    # Update projectiles của enemy (tương tự player)
                    for proj in self.projectiles[:]:
                        proj.update(delta_time)
                        proj.check_collision([player])  # Check hit player (pass list [player])
                        if not proj.alive:
                            self.projectiles.remove(proj)

                elif self.type == 'bomber':
                    # Bomber AI: Di chuyển để vào range ném, ném bom theo hướng player với cooldown
                    if dist > 0:
                        if dist > self.bomb_throw_range_max:
                            # Áp sát để vào range
                            self.direction = base_dir
                        elif dist < self.bomb_throw_range_min:
                            # Né nhẹ nếu quá gần
                            self.direction = -base_dir * 0.5  # Né chậm
                        else:
                            # Trong range: Dừng hoặc di chuyển ngẫu nhiên nhẹ, ném bom
                            self.direction = pygame.Vector2(0, 0)  # Dừng để ném
                            if self.bomb_throw_cooldown <= 0:
                                # Ném bom hướng tới player
                                bomb_dir = base_dir
                                bomb = Projectile(self.rect.centerx, self.rect.centery, bomb_dir, 'bomb',
                                                  self.bomb_damage, self.bomb_speed, BOMB_AOE_RADIUS)
                                self.projectiles.append(bomb)
                                self.bomb_throw_cooldown = 2.5  # Reset cooldown

                    # Update cooldown
                    if self.bomb_throw_cooldown > 0:
                        self.bomb_throw_cooldown -= delta_time

                    # Update projectiles (đã có từ archer, reuse cho bomber)
                    for proj in self.projectiles[:]:
                        proj.update(delta_time)
                        proj.check_collision([player])  # Check AOE damage player
                        if not proj.alive:
                            self.projectiles.remove(proj)

                else:
                    # Fallback random cho type khác
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

        # Vẽ projectiles của enemy
        for proj in self.projectiles:
            proj.draw(screen)