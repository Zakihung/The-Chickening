# modules/managers/level_manager.py
import json
import math
import random
from modules.entities.base_entity import BaseEntity
from modules.entities.enemy import Enemy
from modules.utils.constants import WAVE_COUNT_PER_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT
from modules.utils.helpers import rect_collision
from modules.entities.boss import Boss

class LevelManager:
    def __init__(self):
        """
        Quản lý levels, waves, spawns.
        Load từ data/levels.json.
        """
        with open('data/levels.json', 'r', encoding="utf-8") as f:
            self.levels_data = json.load(f)['levels']
        self.current_level = 0  # Bắt đầu level 1 (index 0)
        self.current_wave = 0
        self.enemies = []  # List all enemies
        self.spawn_points = []  # List destructible spawns (BaseEntity hp)
        self.wave_timer = 0  # Timer spawn wave
        self.max_levels = len(self.levels_data)  # Total levels từ json
        self.is_boss_level = False  # Flag boss every 5
        self.load_level(self.current_level)

    def load_level(self, level_id):
        """Load data level từ json."""
        level = next((l for l in self.levels_data if l['id'] == level_id + 1), None)
        if level:
            self.map_type = level['map_type']
            self.background = level['background']
            self.waves = level['waves'] if not self.is_boss_level else []  # No waves if boss
            self.spawn_points = [BaseEntity(sp['x'], sp['y'], 40, 40, hp=sp['hp']) for sp in level['spawn_points']]
            self.boss_data = level['boss']  # None hoặc dict
            self.current_wave = 0
            self.enemies.clear()
            if self.is_boss_level and self.boss_data:
                # Spawn boss ngay nếu boss level
                boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.boss_data['type'])  # Spawn center
                self.enemies.append(boss)  # Treat boss as enemy

    def next_level(self):
        """Next level logic."""
        self.current_level += 1
        self.is_boss_level = (self.current_level % 5 == 0)
        if self.current_level < self.max_levels:
            self.load_level(self.current_level)
        else:
            print("All levels cleared!")

    def update(self, delta_time, player):
        """Update waves, spawn enemies, check clear."""
        # Spawn wave nếu timer hết và có spawns
        self.wave_timer -= delta_time
        if self.wave_timer <= 0 and self.current_wave < len(self.waves) and self.spawn_points:
            wave = self.waves[self.current_wave]
            for enemy_data in wave['enemies']:
                for _ in range(enemy_data['count']):
                    spawn = random.choice(self.spawn_points)
                    enemy = Enemy(spawn.rect.centerx, spawn.rect.centery, enemy_data['type'])
                    self.enemies.append(enemy)
            self.current_wave += 1
            self.wave_timer = 5.0  # Delay giữa waves

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(delta_time, player)
            if not enemy.alive:
                self.enemies.remove(enemy)

        # Update spawn_points collision với attacks
        for spawn in self.spawn_points[:]:
            # Check melee
            if player.melee_hitbox and rect_collision(spawn.rect, player.melee_hitbox):
                spawn.take_damage(player.melee_damage)
            # Check projectiles
            for proj in player.projectiles:
                if rect_collision(spawn.rect, proj.rect):
                    spawn.take_damage(proj.damage)
                    if proj.type != 'bomb':
                        proj.alive = False
                if proj.type == 'bomb' and proj.exploded:
                    dist = math.hypot(spawn.rect.centerx - proj.rect.centerx, spawn.rect.centery - proj.rect.centery)
                    if dist <= proj.aoe_radius:
                        spawn.take_damage(proj.damage)
            if spawn.hp <= 0:
                self.spawn_points.remove(spawn)

        # Check clear
        if len(self.enemies) == 0 and len(self.spawn_points) == 0 and self.current_wave >= len(self.waves):
            if self.is_boss_level:
                # Boss clear: No boss/minions
                if all(not e.alive for e in self.enemies if isinstance(e, Boss)):
                    self.next_level()
            else:
                self.next_level()

    def draw(self, screen):
        """Draw enemies/spawns."""
        for spawn in self.spawn_points:
            spawn.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)