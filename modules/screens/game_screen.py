# modules/screens/game_screen.py
import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GREEN
from modules.entities.player import Player
from modules.managers.level_manager import LevelManager
from modules.managers.sound_manager import SoundManager
from modules.managers.item_manager import ItemManager
from modules.skills import Skills

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = COLOR_GREEN
        self.player = Player()
        self.level_manager = LevelManager()
        self.player.enemies = self.level_manager.enemies  # Link to level enemies for collision
        self.resources = []  # List Resource
        # self.sound_manager = SoundManager()
        # self.sound_manager.play_music('music_wave.mp3', 0.5)  # Loop music
        # self.sound_manager.play_music('music_wave.mp3')  # Loop with fade
        self.item_manager = ItemManager()
        # Test equip
        self.item_manager.equip_item(self.player, 1)  # Test equip id1
        self.skills = Skills()
        # Test random and apply
        random_skills = self.skills.get_random_skills('melee', 3)
        if random_skills:
            test_id = random_skills[0]['id']
            self.skills.apply_skill(self.player, test_id)

    def update(self, delta_time, keys):
        """Update entities với delta_time và keys."""
        self.player.update(delta_time, keys)
        self.level_manager.update(delta_time, self.player)

        # Update resources
        for res in self.resources[:]:
            res.update(delta_time, self.player)
            if not res.alive:
                self.resources.remove(res)
        # Add dropped from player die
        self.resources.extend(self.player.dropped_resources)
        self.player.dropped_resources.clear()

        # Test damage nếu không invincible (optional)
        if not self.player.invincible:
            self.player.take_damage(0.1)  # Test HP giảm chậm

    def draw_background(self):
        self.level_manager.draw(self.screen)  # Draw bg/obs/enemies/spawns
        self.player.draw(self.screen)
        for res in self.resources:
            res.draw(self.screen)