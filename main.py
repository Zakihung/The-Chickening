import pygame
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK, COLOR_WHITE
)


def main():
    # Khởi tạo Pygame
    pygame.init()

    # Thiết lập window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Chickening - Alpha")

    # Clock để kiểm soát FPS
    clock = pygame.time.Clock()

    # Biến chạy game
    running = True

    # Game loop chính
    while running:
        # Xử lý events (sự kiện)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Thêm xử lý phím cơ bản (ví dụ: ESC để quit)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update logic (sẽ thêm sau)
        # Hiện tại để trống

        # Draw/render (vẽ màn hình)
        screen.fill(COLOR_BLACK)  # Nền đen
        # Ví dụ: Vẽ text test để kiểm tra
        font = pygame.font.SysFont(None, 36)  # Font mặc định
        text = font.render("Welcome to The Chickening! Press ESC to quit.", True, COLOR_WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

        # Flip display để cập nhật
        pygame.display.flip()

        # Giới hạn FPS
        clock.tick(FPS)

    # Quit Pygame khi thoát loop
    pygame.quit()


if __name__ == "__main__":
    main()