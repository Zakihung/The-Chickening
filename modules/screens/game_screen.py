# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN  # Thêm COLOR_GREEN nếu cần

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        # Sau này load background image thực tế
        self.background_color = COLOR_GREEN  # Màu xanh cho "trang trại" tạm thời

    def draw_background(self):
        """Hàm vẽ background đơn giản."""
        self.screen.fill(self.background_color)
        # Ví dụ: Vẽ rect test để simulate background elements
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))  # "Đất" dưới cùng