import pygame
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK, COLOR_WHITE
)
from modules.screens.game_screen import GameScreen
from modules.screens.main_menu import MainMenu
from modules.screens.game_over import GameOver
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
    game_screen = None
    game_over = None

    while running:
        delta_time = clock.get_time() / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if state == 'game' or state == 'options' or state == 'game_over':
                state = 'menu'

        if state == 'menu':
            action = main_menu.update(events)
            if action == 'start':
                state = 'game'
                game_screen = GameScreen(screen, sound_manager)
            elif action == 'options':
                state = 'options'
            elif action == 'quit':
                running = False
            main_menu.draw()
        elif state == 'game':
            game_screen.update(delta_time, keys, events)  # Sửa: Add events as arg
            game_screen.draw_background()
            if not game_screen.player.alive:
                state = 'game_over'
                game_over = GameOver(screen)
        elif state == 'options':
            # Placeholder options: Esc back
            screen.fill(COLOR_BLACK)
            title = pygame.font.SysFont(None, 40).render('Options (Esc to back)', True, COLOR_WHITE)
            screen.blit(title, (SCREEN_WIDTH//2 - 150, 100))
        elif state == 'game_over':
            action = game_over.update(events)
            if action == 'restart':
                state = 'game'
                game_screen = GameScreen(screen, sound_manager)
            elif action == 'quit':
                running = False
            game_over.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()