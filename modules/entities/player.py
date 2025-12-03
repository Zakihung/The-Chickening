# modules/entities/player.py
import random

import pygame
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    PLAYER_HP_DEFAULT, PLAYER_SPEED_DEFAULT, EGGNERGY_MAX, DODGE_COOLDOWN,
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_BLACK, COLOR_RED,
    MELEE_RANGE, PLAYER_DAMAGE_DEFAULT, RANGED_RANGE, BOMB_DAMAGE, BOMB_AOE_RADIUS, BOMB_LIMIT,
    THOC_LOSS_ON_DEATH,
)
from modules.entities.projectile import Projectile
from modules.utils.helpers import rect_collision
from modules.entities.resource import Resource  # Để drop khi die

class Player(BaseEntity):
    def __init__(self):
        """
        Class cho nhân vật chính: Gà con.
        Kế thừa từ BaseEntity, set vị trí giữa màn, load sprite.
        """
        super().__init__(
            x=SCREEN_WIDTH // 2 - 50,  # Trung tâm x
            y=SCREEN_HEIGHT // 2 - 50,  # Trung tâm y
            width=100, height=100,  # Kích thước placeholder, adjust sau
            hp=PLAYER_HP_DEFAULT,
            speed=PLAYER_SPEED_DEFAULT
        )
        # Load sprite (thay chicken.png bằng sprite thực sau)
        try:
            self.image = pygame.image.load('assets/images/player/chicken.png')
            self.image = pygame.transform.scale(self.image, (100, 100))  # Scale phù hợp
            self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.original_image = self.image  # Lưu bản gốc để flip
        except pygame.error as e:
            print(f"Error loading player sprite: {e}")
            self.image = None  # Fallback to placeholder

        # Thuộc tính player-specific
        self.eggnergy = EGGNERGY_MAX  # Năng lượng cho bắn lông
        self.invincible = False  # Flag invincible trong dodge
        self.dodge_speed_multiplier = 2  # Tăng speed gấp 2 khi dodge
        self.dodge_duration = 0  # Timer duration (seconds)
        self.dodge_cooldown_timer = 0  # Timer cooldown (seconds)
        self.melee_cooldown = 0  # Cooldown attack (seconds)
        self.melee_duration = 0  # Duration active hitbox (short, 0.2s)
        self.melee_damage = PLAYER_DAMAGE_DEFAULT  # Sát thương từ constants
        self.melee_hitbox = None  # Rect cho hitbox attack
        self.ranged_cooldown = 0  # Cooldown bắn (seconds)
        self.ranged_cost = 10  # Eggnergy consume mỗi shot
        self.projectiles = []  # List Projectile instances
        self.bomb_cooldown = 0  # Cooldown đẻ bomb (seconds)
        self.bomb_max = BOMB_LIMIT  # Limit max từ constants (3)
        self.bomb_current = self.bomb_max  # Số bomb hiện có
        self.bomb_regen_timer = 0  # Timer regen bomb
        self.enemies = []  # List enemies để check collision

        self.thoc_collected = 0  # Thóc nhặt giữa trận
        self.thoc_stored = 0  # Thóc đã cất an toàn
        self.dropped_resources = []  # List Resource drop khi die (tạm)

    def update(self, delta_time, keys):
        """
        Override update: Xử lý input di chuyển, attacks, dodge.
        :param keys: pygame.key.get_pressed() để check input
        """
        super().update(delta_time)

        # Xử lý input di chuyển
        self.direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x -= 1
            # Flip sprite sang trái
            self.image = pygame.transform.flip(self.original_image, True, False)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x += 1
            # Flip sprite sang phải (gốc)
            self.image = self.original_image

        # Normalize direction để tốc độ chéo = thẳng
        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        # Dodge roll logic
        if keys[pygame.K_SPACE] and self.dodge_cooldown_timer <= 0 and self.dodge_duration <= 0:
            if self.direction.length() > 0:
                self.dodge_duration = 0.5  # 0.5s dodge active
                self.dodge_cooldown_timer = DODGE_COOLDOWN / 1000.0  # 1s cooldown
                self.invincible = True
                self.speed *= self.dodge_speed_multiplier  # Tăng speed

        # Update dodge timers
        if self.dodge_duration > 0:
            self.dodge_duration -= delta_time
            if self.dodge_duration <= 0:
                self.invincible = False
                self.speed /= self.dodge_speed_multiplier
        if self.dodge_cooldown_timer > 0:
            self.dodge_cooldown_timer -= delta_time

        # Melee attack logic (key J)
        if keys[pygame.K_j] and self.melee_cooldown <= 0 and self.melee_duration <= 0:
            if self.direction.length() > 0:
                self.melee_duration = 0.2  # 0.2s active
                self.melee_cooldown = 0.5  # 0.5s cooldown
                # Tạo hitbox phía trước theo direction
                hitbox_offset = self.direction * MELEE_RANGE
                self.melee_hitbox = pygame.Rect(
                    self.rect.centerx + hitbox_offset.x - 25,
                    self.rect.centery + hitbox_offset.y - 25,
                    50, 50  # Kích thước hitbox nhỏ
                )

        # Check melee collision với enemies
        if self.melee_hitbox:
            for enemy in self.enemies:
                if rect_collision(self.melee_hitbox, enemy.rect):
                    enemy.take_damage(self.melee_damage)

        # Update melee timers
        if self.melee_duration > 0:
            self.melee_duration -= delta_time
            if self.melee_duration <= 0:
                self.melee_hitbox = None
        if self.melee_cooldown > 0:
            self.melee_cooldown -= delta_time

        # Ranged attack logic (key K)
        if keys[pygame.K_k] and self.ranged_cooldown <= 0 and self.eggnergy >= self.ranged_cost:
            if self.direction.length() > 0:
                self.ranged_cooldown = 0.3
                self.eggnergy -= self.ranged_cost
                proj = Projectile(self.rect.centerx, self.rect.centery, self.direction, 'ranged', 15, 10)
                self.projectiles.append(proj)

        # Update ranged cooldown
        if self.ranged_cooldown > 0:
            self.ranged_cooldown -= delta_time

        # Bomb attack logic (key L)
        if keys[pygame.K_l] and self.bomb_cooldown <= 0 and self.bomb_current > 0:
            self.bomb_cooldown = 1.0
            self.bomb_current -= 1
            start_x, start_y = self.rect.center
            if self.direction.length() > 0:
                offset = self.direction.normalize() * 50
                start_x += offset.x
                start_y += offset.y
            proj = Projectile(start_x, start_y, self.direction, 'bomb', BOMB_DAMAGE, 5, BOMB_AOE_RADIUS)
            self.projectiles.append(proj)

        # Update bomb cooldown
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= delta_time

        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update(delta_time)
            proj.check_collision(self.enemies)  # Check hit enemies
            if not proj.alive:
                self.projectiles.remove(proj)

        # Regen bomb_current (mỗi 10s)
        self.bomb_regen_timer += delta_time
        if self.bomb_regen_timer >= 10 and self.bomb_current < self.bomb_max:
            self.bomb_current += 1
            self.bomb_regen_timer = 0

        # Regen eggnergy
        self.eggnergy = min(self.eggnergy + 10 * delta_time, EGGNERGY_MAX)

        if self.hp <= 0 and self.alive:
            self.alive = False
            self.die()

    def draw(self, screen):
        """
        Override draw: Vẽ player và thêm eggnergy bar, hiệu ứng dodge.
        """
        if self.image and self.invincible:
            # Hiệu ứng invincible: Tint đỏ (placeholder)
            tint_surface = self.image.copy()
            tint_surface.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(tint_surface, self.rect.topleft)
        else:
            super().draw(screen)  # Bình thường

        # Vẽ melee hitbox nếu active
        if self.melee_hitbox:
            pygame.draw.rect(screen, COLOR_RED, self.melee_hitbox, 2)

        # Vẽ projectiles
        for proj in self.projectiles:
            proj.draw(screen)

        # Vẽ eggnergy bar
        energy_ratio = self.eggnergy / EGGNERGY_MAX
        bar_width = self.rect.width * energy_ratio
        energy_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, 5)  # Dưới HP bar
        pygame.draw.rect(screen, COLOR_YELLOW, energy_bar_rect)
        full_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, self.rect.width, 5)
        pygame.draw.rect(screen, COLOR_BLACK, full_bar_rect, 1)

    def store_thoc(self):
        """Store thóc về chuồng (gọi khi vào safe zone)."""
        self.thoc_stored += self.thoc_collected
        self.thoc_collected = 0

    def die(self):
        """Handle khi chết: Mất 50% thoc_collected, drop remaining."""
        if self.thoc_collected > 0:
            lost = int(self.thoc_collected * THOC_LOSS_ON_DEATH)
            remaining = self.thoc_collected - lost
            self.thoc_collected = 0
            # Drop remaining as Resources around player
            for _ in range(remaining // 5):  # Mỗi 5 thóc 1 Resource
                drop_x = self.rect.centerx + random.randint(-50, 50)
                drop_y = self.rect.centery + random.randint(-50, 50)
                drop = Resource(drop_x, drop_y, 5)
                self.dropped_resources.append(drop)
            print(f"Lost {lost} thóc! Dropped {remaining} to collect again.")
        # Reset HP, position (placeholder)
        self.hp = self.max_hp
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)