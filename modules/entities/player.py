# modules/entities/player.py
import pygame
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    PLAYER_HP_DEFAULT, PLAYER_SPEED_DEFAULT, EGGNERGY_MAX, DODGE_COOLDOWN,
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_BLACK, COLOR_RED, MELEE_RANGE, PLAYER_DAMAGE_DEFAULT, RANGED_RANGE,
)

class Player(BaseEntity):
    def __init__(self):
        """
        Class cho nhân vật chính: Gà con.
        Kế thừa từ BaseEntity, set vị trí giữa màn, load sprite.
        """
        # Gọi super init với vị trí giữa màn, kích thước sprite
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
        self.dodge_cooldown = 0  # Cooldown dodge (milliseconds)
        self.dodge_duration = 0  # Thời gian dodge active (cho invincible)
        # Attacks placeholder (sẽ thêm sau)
        self.melee_damage = 10
        self.ranged_damage = 15
        self.bomb_damage = 50
        self.bomb_count = 3  # Hạn chế trứng nổ
        self.invincible = False  # Flag invincible trong dodge
        self.dodge_speed_multiplier = 2  # Tăng speed gấp 2 khi dodge
        self.dodge_duration = 0  # Timer duration (seconds)
        self.dodge_cooldown_timer = 0  # Timer cooldown (seconds)
        self.melee_cooldown = 0  # Cooldown attack (seconds, ví dụ 0.5s để tránh spam)
        self.melee_duration = 0  # Duration active hitbox (short, 0.2s)
        self.melee_damage = PLAYER_DAMAGE_DEFAULT  # Sát thương từ constants
        self.melee_hitbox = None  # Rect cho hitbox attack
        self.ranged_cooldown = 0  # Cooldown bắn (seconds, ví dụ 0.3s)
        self.ranged_cost = 10  # Eggnergy consume mỗi shot
        self.ranged_damage = 15  # Sát thương trung bình
        self.projectiles = []  # List placeholder cho projectiles (dict với position, direction)

    def update(self, delta_time, keys):
        """
        Override update: Xử lý input di chuyển chi tiết, dodge đầy đủ.
        :param keys: pygame.key.get_pressed() để check input
        """
        super().update(delta_time)  # Gọi base update (di chuyển và clamp)

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
            # Bắt đầu dodge nếu có direction (không đứng yên)
            if self.direction.length() > 0:
                self.dodge_duration = 0.5  # 0.5s dodge active
                self.dodge_cooldown_timer = DODGE_COOLDOWN / 1000.0  # 1s cooldown
                self.invincible = True
                self.speed *= self.dodge_speed_multiplier  # Tăng speed

        # Melee attack logic (key J)
        if keys[pygame.K_j] and self.melee_cooldown <= 0 and self.melee_duration <= 0:
            # Bắt đầu melee nếu có direction
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
                # TODO: Check collision với enemies và apply damage (khi có enemy)

        # Ranged attack logic (key K)
        if keys[pygame.K_k] and self.ranged_cooldown <= 0 and self.eggnergy >= self.ranged_cost:
            # Bắt đầu ranged nếu có direction
            if self.direction.length() > 0:
                self.ranged_cooldown = 0.3  # 0.3s cooldown
                self.eggnergy -= self.ranged_cost
                # Tạo projectile placeholder (dict với rect, direction, speed)
                proj_speed = 10  # Pixels/frame
                proj_rect = pygame.Rect(self.rect.centerx, self.rect.centery, 10, 10)  # Small rect
                proj_dir = self.direction.normalize()  # Hướng bắn
                self.projectiles.append({'rect': proj_rect, 'dir': proj_dir, 'speed': proj_speed})
                # TODO: Tích hợp projectile.py sau, check collision với enemies

        # Update cooldown
        if self.ranged_cooldown > 0:
            self.ranged_cooldown -= delta_time

        # Update projectiles placeholder (di chuyển, remove nếu out screen)
        for proj in self.projectiles[:]:
            # Di chuyển projectile
            proj['rect'].x += proj['dir'].x * proj['speed']
            proj['rect'].y += proj['dir'].y * proj['speed']

            # Tính khoảng cách đã bay từ vị trí bắn ban đầu
            distance_traveled = (
                                        (proj['rect'].centerx - self.rect.centerx) ** 2 +
                                        (proj['rect'].centery - self.rect.centery) ** 2
                                ) ** 0.5

            # Nếu vượt quá tầm bắn HOẶC ra khỏi màn hình → xóa
            if distance_traveled > RANGED_RANGE or \
                    not (0 < proj['rect'].centerx < SCREEN_WIDTH and 0 < proj['rect'].centery < SCREEN_HEIGHT):
                self.projectiles.remove(proj)

        # Update timers
        if self.melee_duration > 0:
            self.melee_duration -= delta_time
            if self.melee_duration <= 0:
                self.melee_hitbox = None
        if self.melee_cooldown > 0:
            self.melee_cooldown -= delta_time

        # Regen eggnergy placeholder
        self.eggnergy = min(self.eggnergy + 10 * delta_time, EGGNERGY_MAX)

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

        if self.melee_hitbox:
            pygame.draw.rect(screen, COLOR_RED, self.melee_hitbox, 2)

        # Vẽ projectiles placeholder (vòng tròn vàng)
        for proj in self.projectiles:
            pygame.draw.circle(screen, COLOR_YELLOW, proj['rect'].center, 5)

        # Vẽ eggnergy bar (giữ nguyên)
        energy_ratio = self.eggnergy / EGGNERGY_MAX
        bar_width = self.rect.width * energy_ratio
        energy_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, 5)
        pygame.draw.rect(screen, COLOR_YELLOW, energy_bar_rect)
        full_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, self.rect.width, 5)
        pygame.draw.rect(screen, COLOR_BLACK, full_bar_rect, 1)