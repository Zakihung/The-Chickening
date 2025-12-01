import pygame
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK, COLOR_WHITE, COLOR_RED
)
from modules.screens.game_screen import GameScreen


def main():
    # Khởi tạo Pygame
    pygame.init()

    # Thiết lập window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Chickening - Alpha")

    # Clock để kiểm soát FPS
    clock = pygame.time.Clock()

    try:
        game_screen = GameScreen(screen)
    except pygame.error as e:
        print(f"Error loading assets: {e}")
        pygame.quit()
        return

    # Biến chạy game và test
    running = True
    background_color = COLOR_BLACK  # Màu nền mặc định

    # Font cho text và FPS
    font = pygame.font.SysFont(None, 36)

    # Game loop chính
    while running:
        # Xử lý events (sự kiện)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:  # Test basic input: Thay đổi màu nền
                    background_color = COLOR_RED if background_color == COLOR_BLACK else COLOR_BLACK

        # Update logic (sẽ thêm sau)
        # Hiện tại để trống

        # Draw/render (vẽ màn hình)
        game_screen.draw_background()
        game_screen.draw_test_sprite()

        # Vẽ text welcome
        text = font.render("Welcome to The Chickening! Press SPACE to toggle color, ESC to quit.", True, COLOR_WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2))

        # Vẽ FPS counter ở góc trên trái
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, COLOR_WHITE)
        screen.blit(fps_text, (10, 10))

        # Flip display để cập nhật
        pygame.display.flip()

        # Giới hạn FPS
        clock.tick(FPS)

    # Quit Pygame khi thoát loop
    pygame.quit()


if __name__ == "__main__":
    main()