# modules/entities/player.py
import pygame
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    PLAYER_HP_DEFAULT, PLAYER_SPEED_DEFAULT, EGGNERGY_MAX,
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
        except pygame.error as e:
            print(f"Error loading player sprite: {e}")
            self.image = None  # Fallback to placeholder

        # Thuộc tính player-specific
        self.eggnergy = EGGNERGY_MAX  # Năng lượng cho bắn lông
        self.dodge_cooldown = 0  # Placeholder cho dodge roll (milliseconds)
        # Attacks placeholder (sẽ thêm sau)
        self.melee_damage = 10
        self.ranged_damage = 15
        self.bomb_damage = 50
        self.bomb_count = 3  # Hạn chế trứng nổ

    def update(self, delta_time, keys):
        """
        Override update: Xử lý input di chuyển, dodge, attacks (placeholder).
        :param keys: pygame.key.get_pressed() để check input
        """
        super().update(delta_time)  # Gọi base update trước

        # Di chuyển dựa trên keys (WASD hoặc arrows)
        self.direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1

        # Normalize nếu di chuyển chéo
        if self.direction.length() > 0:
            self.direction.normalize_ip()

        # Placeholder cho dodge (space), attacks (sẽ thêm ngày sau)
        if keys[pygame.K_SPACE] and self.dodge_cooldown <= 0:
            # Dodge logic: Tăng speed tạm thời, invincible short time
            pass  # Implement sau

    def draw(self, screen):
        """
        Override draw: Vẽ player và thêm eggnergy bar.
        """
        super().draw(screen)  # Gọi base draw (sprite và HP bar)

        # Vẽ eggnergy bar dưới HP bar
        if self.eggnergy > 0:
            energy_ratio = self.eggnergy / EGGNERGY_MAX
            bar_width = self.rect.width * energy_ratio
            energy_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, 5)  # Dưới HP bar
            pygame.draw.rect(screen, COLOR_YELLOW, energy_bar_rect)
            full_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, self.rect.width, 5)
            pygame.draw.rect(screen, COLOR_BLACK, full_bar_rect, 1)