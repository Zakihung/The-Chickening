# modules/entities/player.py
import pygame
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    PLAYER_HP_DEFAULT, PLAYER_SPEED_DEFAULT, EGGNERGY_MAX, DODGE_COOLDOWN,
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_BLACK
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

    def update(self, delta_time, keys):
        """
        Override update: Xử lý input di chuyển chi tiết, dodge placeholder.
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

        # Normalize direction để tốc độ chéo = thẳng (sqrt(2) fix)
        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        # Placeholder cho dodge roll (SPACE)
        if keys[pygame.K_SPACE] and self.dodge_cooldown <= 0:
            # Bắt đầu dodge: Tăng speed tạm, set duration, cooldown
            self.speed *= 2  # Tốc độ lăn né nhanh gấp đôi
            self.dodge_duration = 0.5  # 0.5 giây invincible (sẽ dùng timer)
            self.dodge_cooldown = DODGE_COOLDOWN / 1000  # Convert ms to seconds
            # TODO: Thêm invincible flag

        # Update cooldown và duration (dùng delta_time)
        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= delta_time
        if self.dodge_duration > 0:
            self.dodge_duration -= delta_time
            if self.dodge_duration <= 0:
                self.speed = PLAYER_SPEED_DEFAULT  # Reset speed sau dodge

        # Regen eggnergy placeholder (tăng dần theo thời gian)
        self.eggnergy = min(self.eggnergy + 10 * delta_time, EGGNERGY_MAX)

    def draw(self, screen):
        """
        Override draw: Vẽ player và thêm eggnergy bar.
        """
        super().draw(screen)  # Gọi base draw (sprite và HP bar)

        # Vẽ eggnergy bar dưới HP bar
        energy_ratio = self.eggnergy / EGGNERGY_MAX
        bar_width = self.rect.width * energy_ratio
        energy_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, 5)  # Dưới HP bar
        pygame.draw.rect(screen, COLOR_YELLOW, energy_bar_rect)
        full_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, self.rect.width, 5)
        pygame.draw.rect(screen, COLOR_BLACK, full_bar_rect, 1)