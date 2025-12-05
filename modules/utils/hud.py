import pygame

from modules.utils.constants import COLOR_RED, COLOR_GREEN, COLOR_BLUE, EGGNERGY_MAX, COLOR_YELLOW, COLOR_BLACK, \
    SCREEN_WIDTH, COLOR_WHITE


class Hud:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont(None, 30)

    def draw(self):
        # HP bar
        pygame.draw.rect(self.screen, COLOR_RED, (10, 10, 200, 20))
        hp_width = 200 * (self.player.hp / self.player.max_hp)
        pygame.draw.rect(self.screen, COLOR_GREEN, (10, 10, hp_width, 20))
        # Energy
        pygame.draw.rect(self.screen, COLOR_BLUE, (10, 40, 200, 20))
        energy_width = 200 * (self.player.eggnergy / EGGNERGY_MAX)
        pygame.draw.rect(self.screen, COLOR_YELLOW, (10, 40, energy_width, 20))
        # Thóc text
        thoc_text = self.font.render(f"Thóc: {self.player.thoc_collected} / Stored: {self.player.thoc_stored}", True, COLOR_WHITE)
        self.screen.blit(thoc_text, (10, 70))
        # Minimap placeholder
        pygame.draw.rect(self.screen, COLOR_BLACK, (SCREEN_WIDTH - 150, 10, 140, 140))
        # Draw player/enemies on minimap (scale pos /10)