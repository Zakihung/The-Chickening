import pygame
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK, COLOR_WHITE
)
from modules.screens.game_screen import GameScreen
from modules.screens.main_menu import MainMenu
from modules.managers.sound_manager import SoundManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Chickening - Alpha")
    clock = pygame.time.Clock()

    sound_manager = SoundManager()

    running = True
    state = 'menu'
    main_menu = MainMenu(screen)
    game_screen = None  # Lazy init
    options_screen = None  # Placeholder

    while running:
        delta_time = clock.get_time() / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if state == 'menu':
            action = main_menu.update(events)
            if action == 'start':
                state = 'game'
                game_screen = GameScreen(screen, sound_manager)  # Pass sound
            elif action == 'options':
                state = 'options'
                # options_screen = OptionsScreen(screen)
            elif action == 'quit':
                running = False
            main_menu.draw()
        elif state == 'game':
            keys = pygame.key.get_pressed()
            game_screen.update(delta_time, keys)
            game_screen.draw_background()
        elif state == 'options':
            # Placeholder options: Back button
            action = options_screen.update(events) if options_screen else 'menu'  # Back to menu
            if action == 'back':
                state = 'menu'
            options_screen.draw() if options_screen else main_menu.draw()  # Placeholder draw

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()