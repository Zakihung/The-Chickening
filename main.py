import pygame
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK, COLOR_WHITE
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

    # Biến chạy game
    running = True

    # Game loop chính
    while running:
        delta_time = clock.get_time() / 1000.0  # Seconds since last frame

        # Xử lý events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Lấy keys
        keys = pygame.key.get_pressed()

        # Update game_screen với delta_time và keys
        game_screen.update(delta_time, keys)

        # Draw
        game_screen.draw_background()

        # Flip display
        pygame.display.flip()

        # Giới hạn FPS
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()