# modules/entities/enemy.py
import math
import pygame
import random
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    ENEMY_HP_BASE, ENEMY_SPEED_BASE, COLOR_RED, DROP_THO_RATE, SCREEN_WIDTH, SCREEN_HEIGHT
)
from modules.utils.helpers import rect_collision
from modules.entities.projectile import Projectile
from modules.entities.resource import Resource

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
        self.shield_turn_timer = 0  # Timer quay lưng (expose back)
        self.shield_turn_duration = 0  # Thời gian expose back (1-2s)
        self.shield_cooldown = 0  # Cooldown trước khi turn back lại
        self.back_weak_mult = 2.0  # Sát thương x2 nếu hit back
        self.front_resist_mult = 0.2  # Giảm 80% damage nếu hit front
        self.shield_hp = 50  # HP riêng cho khiên (giảm khi hit front)
        self.shield_max_hp = 50
        self.facing_player = True  # Flag quay mặt player (shield front)
        self.fire_cast_cooldown = 0  # Cooldown cast lửa (2s)
        self.buff_cooldown = 0  # Cooldown buff (5s)
        self.barrier_cooldown = 0  # Cooldown tạo vòng (4s)
        self.fire_damage = 25  # Sát thương lửa
        self.fire_speed = 7
        self.buff_amount = 1.5  # Tăng speed/HP x1.5 temp 5s
        self.buff_duration = 0  # Self buff timer
        self.barrier_radius = 80  # Bán kính vòng cản
        self.barrier_projectiles = []  # List barrier projs riêng (persistent)
        self.allies = []  # List enemies để buff (placeholder, pass từ manager sau)
        self.dropped = False  # Flag để tránh drop multi

    def update(self, delta_time, player=None):
        """
        Override update: AI simple - di chuyển ngẫu nhiên, change direction random.
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
                    offset = math.sin(self.time * self.zigzag_frequency) * self.zigzag_amplitude / dist  # Scale với dist
                    self.direction = pygame.Vector2(base_dir.x, base_dir.y + offset)
                    self.direction.normalize_ip() if self.direction.length() > 0 else None
                    self.speed = ENEMY_SPEED_BASE * 1.5  # Tốc độ nhanh hơn cho runner

                    # Attack nếu trong range (placeholder damage)
                    if dist < self.attack_range and not player.invincible:
                        # self.sound_manager.play_sfx('auu')
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
                            arrow = Projectile(self.rect.centerx, self.rect.centery, arrow_dir, 'ranged', self.arrow_damage, self.arrow_speed)
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
                                bomb = Projectile(self.rect.centerx, self.rect.centery, bomb_dir, 'bomb', self.bomb_damage, self.bomb_speed, BOMB_AOE_RADIUS)
                                self.projectiles.append(bomb)
                                self.bomb_throw_cooldown = 2.5  # Reset cooldown

                    # Update cooldown
                    if self.bomb_throw_cooldown > 0:
                        self.bomb_throw_cooldown -= delta_time

                    # Update projectiles (đã có từ archer, reuse cho bomber)
                    for proj in self.projectiles[:]:
                        proj.update(delta_time)
                        proj.check_collision([player])
                        if not proj.alive:
                            self.projectiles.remove(proj)

                elif self.type == 'shield':
                    # Shield AI: Quay mặt player (shield front), random turn back expose weak
                    if dist > 0:
                        base_dir = pygame.Vector2(dx / dist, dy / dist)
                        self.direction = -base_dir  # Quay mặt player (direction ngược = face to)

                    # Turn back logic: Random expose back
                    if self.shield_turn_duration <= 0 and self.shield_cooldown <= 0:
                        if random.random() < 0.01:  # 1% chance mỗi frame ~1s average
                            self.facing_player = False  # Turn back
                            self.shield_turn_duration = random.uniform(1, 2)
                    if self.shield_turn_duration > 0:
                        self.shield_turn_duration -= delta_time
                        if self.shield_turn_duration <= 0:
                            self.shield_cooldown = 3.0  # Cooldown 3s trước turn back tiếp
                            self.facing_player = True
                    if self.shield_cooldown > 0:
                        self.shield_cooldown -= delta_time

                    # Attack melee nếu gần và facing_player=False (back attack?)
                    if dist < self.attack_range and not self.facing_player and not player.invincible:
                        # self.sound_manager.play_sfx('auu')
                        player.take_damage(self.attack_damage * 1.5)  # Stronger back attack

                    self.speed = ENEMY_SPEED_BASE * 0.8  # Chậm hơn vì giáp nặng

                elif self.type == 'mage':
                    # Mage AI: Di chuyển chậm, cast lửa/buff/barrier theo cooldown
                    if dist > 0:
                        base_dir = pygame.Vector2(dx / dist, dy / dist)
                        self.direction = base_dir * 0.5  # Áp sát chậm

                    self.speed = ENEMY_SPEED_BASE * 0.6  # Chậm vì pháp sư

                    # Cast lửa (ranged proj hướng player)
                    if self.fire_cast_cooldown <= 0:
                        fire = Projectile(self.rect.centerx, self.rect.centery, base_dir, 'ranged', self.fire_damage, self.fire_speed)
                        self.projectiles.append(fire)
                        self.fire_cast_cooldown = 2.0

                    # Buff allies/self (tăng speed nếu buff_duration >0)
                    if self.buff_duration > 0:
                        self.speed *= self.buff_amount  # Self buff (sẽ apply allies sau)
                        self.buff_duration -= delta_time
                    if self.buff_cooldown <= 0:
                        self.buff_duration = 5.0  # Buff 5s
                        self.buff_cooldown = 10.0  # Cooldown 10s
                        # TODO: Loop allies: ally.speed *= buff_amount; ally.buff_timer = 5

                    # Tạo vòng cản (8 projs quanh self)
                    if self.barrier_cooldown <= 0:
                        for i in range(8):
                            angle = (i / 8) * 2 * math.pi
                            barrier_dir = pygame.Vector2(math.cos(angle), math.sin(angle))
                            barrier_pos = self.rect.center + barrier_dir * self.barrier_radius
                            barrier = Projectile(barrier_pos[0], barrier_pos[1], pygame.Vector2(0,0), 'ranged', 15, 0)  # Speed 0 = stationary
                            barrier.aoe_radius = 20  # Small damage circle
                            self.barrier_projectiles.append(barrier)
                        self.barrier_cooldown = 8.0  # Cooldown 8s

                    # Update barrier projs (persistent 5s each)
                    for barrier in self.barrier_projectiles[:]:
                        barrier.update(delta_time)
                        barrier.check_collision([player])  # Damage player chạm
                        if not barrier.alive:  # Set alive=False sau 5s trong Projectile?
                            self.barrier_projectiles.remove(barrier)

                    # Update cooldowns
                    self.fire_cast_cooldown = max(0, self.fire_cast_cooldown - delta_time)
                    self.buff_cooldown = max(0, self.buff_cooldown - delta_time)
                    self.barrier_cooldown = max(0, self.barrier_cooldown - delta_time)

                    # Update main projectiles (lửa)
                    for proj in self.projectiles[:]:
                        proj.update(delta_time)
                        proj.check_collision([player])
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
            # self.sound_manager.play_sfx('auu')
            player.take_damage(10)  # Damage placeholder khi chạm

        # Drop thóc khi chết (placeholder print)
        if not self.alive and not self.dropped:
            if random.random() < DROP_THO_RATE:
                thoc = Resource(self.rect.centerx, self.rect.centery, random.randint(5, 20))
                # Add to global resources list (placeholder in game_screen)
            self.dropped = True  # Avoid multi-drop

    def is_back_hit(self, attacker_pos):
        """
        Check nếu hit từ phía sau (dot product < 0).
        :param attacker_pos: Vị trí attacker (projectile hoặc player)
        """
        to_attacker = pygame.Vector2(attacker_pos[0] - self.rect.centerx, attacker_pos[1] - self.rect.centery)
        to_attacker.normalize_ip()
        facing_dir = -self.direction if self.facing_player else self.direction  # Front/back dir
        dot = to_attacker.dot(facing_dir)
        return dot < 0  # Back hit nếu góc >90 độ

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

        # Vẽ barrier riêng (color tím)
        for barrier in self.barrier_projectiles:
            barrier.draw(screen)