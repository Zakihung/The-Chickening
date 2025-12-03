# modules/managers/level_manager.py
import json
import random

from modules.entities.base_entity import BaseEntity
from modules.entities.enemy import Enemy
from modules.utils.constants import WAVE_COUNT_PER_LEVEL
from modules.utils.helpers import rect_collision

class LevelManager:
    def __init__(self):
        """
        Quản lý levels, waves, spawns.
        Load từ data/levels.json.
        """
        with open('data/levels.json', 'r', encoding='utf-8') as f:
            self.levels_data = json.load(f)['levels']
        self.current_level = 0  # Bắt đầu level 1 (index 0)
        self.current_wave = 0
        self.enemies = []  # List all enemies
        self.spawn_points = []  # List destructible spawns (BaseEntity hp)
        self.wave_timer = 0  # Timer spawn wave
        self.load_level(self.current_level)

    def load_level(self, level_id):
        """Load data level từ json."""
        level = next((l for l in self.levels_data if l['id'] == level_id + 1), None)  # id 1 = index 0
        if level:
            self.map_type = level['map_type']
            self.background = level['background']
            self.waves = level['waves']
            self.spawn_points = [BaseEntity(sp['x'], sp['y'], 30, 30, hp=sp['hp']) for sp in level['spawn_points']]
            self.boss = level['boss']  # None hoặc dict
            self.current_wave = 0
            self.enemies.clear()

    def update(self, delta_time, player):
        """Update waves, spawn enemies, check clear."""
        # Spawn wave nếu timer hết
        self.wave_timer -= delta_time
        if self.wave_timer <= 0 and self.current_wave < len(self.waves):
            wave = self.waves[self.current_wave]
            for enemy_data in wave['enemies']:
                for _ in range(enemy_data['count']):
                    spawn = random.choice(self.spawn_points)
                    enemy = Enemy(spawn.rect.centerx, spawn.rect.centery, enemy_data['type'])
                    self.enemies.append(enemy)
            self.current_wave += 1
            self.wave_timer = 5.0  # Delay giữa waves (adjust)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(delta_time, player)
            if not enemy.alive:
                self.enemies.remove(enemy)

        # Check clear wave: No enemies and all spawns destroyed? (placeholder no enemies)
        if len(self.enemies) == 0 and self.current_wave >= len(self.waves):
            # Clear level, next or boss
            pass

    def draw(self, screen):
        """Draw enemies/spawns."""
        for spawn in self.spawn_points:
            spawn.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)