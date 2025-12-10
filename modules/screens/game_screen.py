# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN, COLOR_WHITE
from modules.entities.player import Player
from modules.managers.level_manager import LevelManager
from modules.managers.item_manager import ItemManager
from modules.skills import Skills  # Thêm import Skills
from modules.screens.safe_zone import SafeZone
from modules.utils.hud import Hud


class GameScreen:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.background_color = COLOR_GREEN

        # Khởi tạo các manager và entity theo đúng thứ tự
        self.player = Player(self.sound_manager)
        self.level_manager = LevelManager(self.sound_manager)
        self.item_manager = ItemManager()
        self.skills = Skills()  # Thêm dòng này để khởi tạo Skills

        # Liên kết
        self.player.enemies = self.level_manager.enemies

        # HUD và các danh sách
        self.resources = []
        self.popups = []  # Thêm dòng này để khởi tạo popups
        self.hud = Hud(self.screen, self.player, self.level_manager.enemies, self.level_manager, self)

        # Trạng thái game
        self.paused = False
        self.safe_zone = None
        self.font = pygame.font.SysFont(None, 50)
        self.score = 0
        self.kills = 0

    def update(self, delta_time, keys, events):
        """Update with events for safe_zone."""
        if keys[pygame.K_p]:
            self.paused = not self.paused

        if self.paused:
            return

        if keys[pygame.K_s] and not self.safe_zone:
            self.safe_zone = SafeZone(self.screen, self.player, self.item_manager, self.skills)  # Pass item/skills if need

        if self.safe_zone:
            action = self.safe_zone.update(events)
            if action == 'back' or keys[pygame.K_ESCAPE]:
                self.safe_zone = None
            return

        self.player.update(delta_time, keys)
        self.level_manager.update(delta_time, self.player)

        for res in self.resources[:]:
            res.update(delta_time, self.player)
            if not res.alive:
                self.resources.remove(res)
        self.resources.extend(self.player.dropped_resources)
        self.player.dropped_resources.clear()

        if keys[pygame.K_e] and self.player.inventory:
            item_id = self.player.inventory.pop(0)
            self.item_manager.equip_item(self.player, item_id)

        # Tính score (placeholder)
        self.score = (
                self.player.thoc_collected +
                self.player.thoc_stored +
                (self.level_manager.current_level * 100) +
                (self.kills * 10)
        )

        # Update HUD with delta_time for popups/FPS
        self.hud.update(delta_time)

    def draw_background(self):
        # Dùng background từ level_manager (đã có bg + obstacles + spawns)
        self.level_manager.draw(self.screen)

        # Vẽ player và resources
        self.player.draw(self.screen)
        for res in self.resources:
            res.draw(self.screen)

        # HUD
        self.hud.draw()

        # Paused overlay
        if self.paused:
            paused_text = self.font.render('Paused', True, COLOR_WHITE)
            text_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(paused_text, text_rect)

        # Safe zone overlay
        if self.safe_zone:
            self.safe_zone.draw()