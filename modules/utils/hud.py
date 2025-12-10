# modules/utils/hud.py
import pygame

from modules.utils.constants import COLOR_RED, COLOR_GREEN, COLOR_BLUE, EGGNERGY_MAX, COLOR_YELLOW, COLOR_BLACK, \
    SCREEN_WIDTH, COLOR_WHITE, SCREEN_HEIGHT


class Hud:
    def __init__(self, screen, player, enemies, level_manager, game_screen):
        self.screen = screen
        self.player = player
        self.enemies = enemies  # List for minimap
        self.level_manager = level_manager  # For wave/level
        self.game_screen = game_screen  # For score/popups
        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 20)
        self.minimap_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 140)
        self.minimap_scale = 0.1  # Scale pos /10
        self.inventory_rect = pygame.Rect(10, SCREEN_HEIGHT - 100, 200, 80)  # Inventory UI
        self.skills_rect = pygame.Rect(220, SCREEN_HEIGHT - 100, 200, 80)  # Skills UI

    def update(self, delta_time):
        """Update popups fade and FPS."""
        self.fps = int(1 / delta_time) if delta_time > 0 else 0
        for popup in self.game_screen.popups[:]:
            popup['timer'] -= delta_time
            if popup['timer'] <= 0:
                self.game_screen.popups.remove(popup)

    def draw(self):
        # HP bar
        pygame.draw.rect(self.screen, COLOR_RED, (10, 10, 200, 20))
        hp_width = 200 * (self.player.hp / self.player.max_hp)
        pygame.draw.rect(self.screen, COLOR_GREEN, (10, 10, hp_width, 20))
        hp_text = self.font.render(f"HP: {int(self.player.hp)}/{self.player.max_hp}", True, COLOR_WHITE)
        self.screen.blit(hp_text, (220, 10))
        # Energy
        pygame.draw.rect(self.screen, COLOR_BLUE, (10, 40, 200, 20))
        energy_width = 200 * (self.player.eggnergy / EGGNERGY_MAX)
        pygame.draw.rect(self.screen, COLOR_YELLOW, (10, 40, energy_width, 20))
        # Thóc text
        thoc_text = self.font.render(f"Thóc: {self.player.thoc_collected} / Stored: {self.player.thoc_stored}", True, COLOR_WHITE)
        self.screen.blit(thoc_text, (10, 70))
        # Score
        score_text = self.font.render(f"Score: {self.game_screen.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 10))
        # Wave/Level
        wave_text = self.font.render(f"Level: {self.level_manager.current_level} Wave: {self.level_manager.current_wave}/{len(self.level_manager.waves)}", True, COLOR_WHITE)
        self.screen.blit(wave_text, (SCREEN_WIDTH//2 - 150, 10))
        # FPS
        fps_text = self.font.render(f"FPS: {self.fps}", True, COLOR_WHITE)
        self.screen.blit(fps_text, (10, SCREEN_HEIGHT - 30))
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
        # Inventory UI
        pygame.draw.rect(self.screen, COLOR_BLACK, self.inventory_rect)
        inv_text = self.small_font.render('Inventory', True, COLOR_WHITE)
        self.screen.blit(inv_text, (self.inventory_rect.x + 5, self.inventory_rect.y + 5))
        for i, item_id in enumerate(self.player.inventory[:4]):  # Show 4
            item_rect = pygame.Rect(self.inventory_rect.x + 5 + i*50, self.inventory_rect.y + 30, 40, 40)
            pygame.draw.rect(self.screen, COLOR_WHITE, item_rect)
            id_text = self.small_font.render(str(item_id), True, COLOR_BLACK)
            self.screen.blit(id_text, item_rect.center)
        # Skills UI
        pygame.draw.rect(self.screen, COLOR_BLACK, self.skills_rect)
        skills_text = self.small_font.render('Skills', True, COLOR_WHITE)
        self.screen.blit(skills_text, (self.skills_rect.x + 5, self.skills_rect.y + 5))
        for i, skill_id in enumerate(self.player.unlocked_skills[:4]):
            skill_rect = pygame.Rect(self.skills_rect.x + 5 + i*50, self.skills_rect.y + 30, 40, 40)
            pygame.draw.rect(self.screen, COLOR_WHITE, skill_rect)
            id_text = self.small_font.render(str(skill_id), True, COLOR_BLACK)
            self.screen.blit(id_text, skill_rect.center)
        # Damage popups
        for popup in self.game_screen.popups:
            alpha = int(255 * (popup['timer'] / 1.0))
            text_surf = self.font.render(popup['text'], True, popup['color'])
            text_surf.set_alpha(alpha)
            self.screen.blit(text_surf, popup['pos'])