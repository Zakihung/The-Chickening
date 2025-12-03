import pygame
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK, COLOR_WHITE
)
from modules.screens.game_screen import GameScreen
from modules.screens.main_menu import MainMenu

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
    state = 'menu'  # 'menu', 'game', 'options'
    main_menu = MainMenu(screen)
    # Game loop chính
    while running:
        delta_time = clock.get_time() / 1000.0  # Seconds since last frame
        events = pygame.event.get()  # Get events once
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        if state == 'menu':
            action = main_menu.update(events)
            if action == 'start':
                state = 'game'
            elif action == 'options':
                state = 'options'  # Placeholder
            elif action == 'quit':
                running = False
            main_menu.draw()
        elif state == 'game':
            keys = pygame.key.get_pressed()
            game_screen.update(delta_time, keys)
            game_screen.draw_background()
        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()