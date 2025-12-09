import pygame
from modules.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK, COLOR_WHITE
)
from modules.screens.game_screen import GameScreen
from modules.screens.main_menu import MainMenu
from modules.screens.game_over import GameOver
from modules.screens.options import Options
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
    options = None
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
    fade_alpha = 0
    fade_speed = 5  # Alpha change per frame

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
                fade_alpha = 255  # Start fade

        if state == 'menu':
            action = main_menu.update(events)
            if action == 'start':
                state = 'game'
                game_screen = GameScreen(screen, sound_manager)
                fade_alpha = 255
            elif action == 'options':
                state = 'options'
                options = Options(screen, sound_manager)
                fade_alpha = 255
            elif action == 'quit':
                running = False
            main_menu.draw()
        elif state == 'game':
            game_screen.update(delta_time, keys, events)
            game_screen.draw_background()
            if not game_screen.player.alive:
                state = 'game_over'
                game_over = GameOver(screen, game_screen.score)
                fade_alpha = 255
        elif state == 'options':
            action = options.update(events)
            if action == 'back':
                state = 'menu'
                fade_alpha = 255
            options.draw()
        elif state == 'game_over':
            action = game_over.update(events)
            if action == 'restart':
                state = 'game'
                game_screen = GameScreen(screen, sound_manager)
                fade_alpha = 255
            elif action == 'quit':
                running = False
            game_over.draw()

        # Fade transition if alpha >0
        if fade_alpha > 0:
            fade_surface.fill((0, 0, 0, fade_alpha))
            screen.blit(fade_surface, (0, 0))
            fade_alpha -= fade_speed
            if fade_alpha < 0:
                fade_alpha = 0

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()