import pygame

from modules.utils.constants import COLOR_RED, COLOR_GREEN, COLOR_BLUE, EGGNERGY_MAX, COLOR_YELLOW, COLOR_BLACK, \
    SCREEN_WIDTH, COLOR_WHITE


class Hud:
    def __init__(self, screen, player, enemies):
        self.screen = screen
        self.player = player
        self.enemies = enemies  # List for minimap
        self.font = pygame.font.SysFont(None, 30)
        self.minimap_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 140)
        self.minimap_scale = 0.1  # Scale pos /10

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
        # Minimap
        pygame.draw.rect(self.screen, COLOR_BLACK, self.minimap_rect)
        # Player dot green center minimap
        player_mini_x = self.minimap_rect.centerx
        player_mini_y = self.minimap_rect.centery
        pygame.draw.circle(self.screen, COLOR_GREEN, (player_mini_x, player_mini_y), 5)
        # Enemies dots red scale pos
        for enemy in self.enemies:
            rel_x = (enemy.rect.centerx - self.player.rect.centerx) * self.minimap_scale
            rel_y = (enemy.rect.centery - self.player.rect.centery) * self.minimap_scale
            enemy_mini_x = player_mini_x + rel_x
            enemy_mini_y = player_mini_y + rel_y
            if self.minimap_rect.collidepoint(enemy_mini_x, enemy_mini_y):
                pygame.draw.circle(self.screen, COLOR_RED, (enemy_mini_x, enemy_mini_y), 3)