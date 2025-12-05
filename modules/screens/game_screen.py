# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN, COLOR_WHITE
from modules.entities.player import Player
from modules.managers.level_manager import LevelManager
from modules.managers.item_manager import ItemManager
from modules.screens.safe_zone import SafeZone
from modules.utils.hud import Hud

class GameScreen:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.background_color = COLOR_GREEN
        self.player = Player(self.sound_manager)
        self.level_manager = LevelManager(self.sound_manager)
        self.player.enemies = self.level_manager.enemies
        self.resources = []
        self.item_manager = ItemManager()
        self.hud = Hud(self.screen, self.player, self.level_manager.enemies)
        self.paused = False
        self.safe_zone = None
        self.font = pygame.font.SysFont(None, 50)  # For paused text

    def update(self, delta_time, keys, events):
        """Update with events for safe_zone."""
        if keys[pygame.K_p]:  # Toggle pause
            self.paused = not self.paused

        if self.paused:
            return  # No update if paused

        if keys[pygame.K_s] and not self.safe_zone:
            self.safe_zone = SafeZone(self.screen, self.player)

        if self.safe_zone:
            action = self.safe_zone.update(events)
            if action == 'back' or keys[pygame.K_ESCAPE]:
                self.safe_zone = None
            return  # No other update in safe_zone

        self.player.update(delta_time, keys)
        self.level_manager.update(delta_time, self.player)

        for res in self.resources[:]:
            res.update(delta_time, self.player)
            if not res.alive:
                self.resources.remove(res)
        self.resources.extend(self.player.dropped_resources)
        self.player.dropped_resources.clear()

        # Equip from inventory on key E
        if keys[pygame.K_e] and self.player.inventory:
            item_id = self.player.inventory.pop(0)  # Equip first
            self.item_manager.equip_item(self.player, item_id)

    def draw_background(self):
        self.screen.fill(self.background_color)
        self.level_manager.draw(self.screen)
        self.player.draw(self.screen)
        for res in self.resources:
            res.draw(self.screen)
        self.hud.draw()
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))  # Grass placeholder

        if self.paused:
            paused_text = self.font.render('Paused', True, COLOR_WHITE)
            self.screen.blit(paused_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

        if self.safe_zone:
            self.safe_zone.draw()