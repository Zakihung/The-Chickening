# modules/screens/game_screen.py
import pygame

from modules.skills import Skills
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.entities.player import Player
from modules.managers.level_manager import LevelManager
from modules.managers.item_manager import ItemManager
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
        self.skills = Skills()
        self.hud = Hud(self.screen, self.player)

    def update(self, delta_time, keys):
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

        if keys[pygame.K_b]:
            self.skills.choose_branch(self.player, 'bomb')  # Test change branch

        if not self.player.invincible:
            self.player.take_damage(0.1)  # Test, remove later

    def draw_background(self):
        self.screen.fill(self.background_color)
        self.level_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.hud.draw()
        for res in self.resources:
            res.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 100, 0), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))  # Grass placeholder