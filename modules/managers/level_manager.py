# modules/managers/level_manager.py
import json
import math
import random

import pygame

from modules.entities.base_entity import BaseEntity
from modules.entities.enemy import Enemy
from modules.utils.constants import WAVE_COUNT_PER_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_PATH
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
        self.current_level = 0
        self.current_wave = 0
        self.enemies = []
        self.spawn_points = []
        self.obstacles = []           # ← Ở đây
        self.wave_timer = 0
        self.max_levels = len(self.levels_data)
        self.is_boss_level = False
        self.background_image = None  # ← Ở đây
        self.load_level(self.current_level)

    def load_level(self, level_id):
        """Load data level từ json."""
        level = next((l for l in self.levels_data if l['id'] == level_id + 1), None)
        if level:
            self.map_type = level['map_type']
            self.background = level.get('background', None)

            # === PHẦN SỬA TẠI ĐÂY ===
            bg_path = None
            if self.background:
                import os
                bg_path = os.path.join(IMAGES_PATH, 'backgrounds', self.background)
                if os.path.exists(bg_path):
                    try:
                        self.background_image = pygame.image.load(bg_path)
                        self.background_image = pygame.transform.scale(self.background_image,
                                                                       (SCREEN_WIDTH, SCREEN_HEIGHT))
                    except pygame.error as e:
                        print(f"Không load được background {bg_path}: {e}")
                        self.background_image = None
                else:
                    print(f"Không tìm thấy file background: {bg_path}")
                    self.background_image = None

            # Fallback: Nếu không có ảnh → tạo surface màu xanh lá (farm) hoặc xám
            if self.background_image is None:
                self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                if self.map_type == 'farm':
                    self.background_image.fill((34, 139, 34))  # Xanh lá cây đồng cỏ
                elif self.map_type == 'forest':
                    self.background_image.fill((0, 100, 0))  # Xanh rừng
                elif self.map_type == 'village':
                    self.background_image.fill((139, 90, 43))  # Nâu đất làng
                elif self.map_type == 'volcano':
                    self.background_image.fill((100, 0, 0))  # Đỏ núi lửa
                else:
                    self.background_image.fill((50, 50, 50))

            # === Kết thúc phần sửa ===

            # Load obstacles dựa trên map_type (giữ nguyên code cũ của bạn)
            self.obstacles.clear()
            if self.map_type == 'farm':
                for _ in range(5):
                    obs = BaseEntity(random.randint(100, SCREEN_WIDTH - 100),
                                     random.randint(100, SCREEN_HEIGHT - 100), 80, 80, hp=30)
                    self.obstacles.append(obs)
            elif self.map_type == 'forest':
                for _ in range(12):
                    obs = BaseEntity(random.randint(50, SCREEN_WIDTH - 50),
                                     random.randint(50, SCREEN_HEIGHT - 50), 60, 60, hp=20)
                    self.obstacles.append(obs)
            # ... thêm các map khác nếu muốn

            # Phần còn lại giữ nguyên
            self.waves = level['waves'] if not self.is_boss_level else []
            self.spawn_points = [BaseEntity(sp['x'], sp['y'], 40, 40, hp=sp['hp']) for sp in level['spawn_points']]
            self.boss_data = level['boss']
            self.current_wave = 0
            self.enemies.clear()
            if self.is_boss_level and self.boss_data:
                boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.boss_data['type'])
                self.enemies.append(boss)

    def next_level(self):
        """Next level logic."""
        self.current_level += 1
        self.is_boss_level = (self.current_level % 5 == 0)
        # self.sound_manager.stop_music()  # Fade out on level change
        # self.sound_manager.play_music('music_wave.mp3')  # Play new (placeholder same)
        if self.current_level < self.max_levels:
            self.load_level(self.current_level)
        else:
            print("All levels cleared!")

    def update(self, delta_time, player):
        """Update waves, spawn enemies, check clear."""
        # Update obstacles collision với attacks (similar spawns)
        for obs in self.obstacles[:]:
            if player.melee_hitbox and rect_collision(obs.rect, player.melee_hitbox):
                obs.take_damage(player.melee_damage)
            for proj in player.projectiles:
                if rect_collision(obs.rect, proj.rect):
                    obs.take_damage(proj.damage)
                    if proj.type != 'bomb':
                        proj.alive = False
                if proj.type == 'bomb' and proj.exploded:
                    dist = math.hypot(obs.rect.centerx - proj.rect.centerx, obs.rect.centery - proj.rect.centery)
                    if dist <= proj.aoe_radius:
                        obs.take_damage(proj.damage)
            if obs.hp <= 0:
                self.obstacles.remove(obs)
                # Drop thóc placeholder if destructible

        # Block movement: Check collision player/enemies with obstacles
        for obs in self.obstacles:
            if rect_collision(player.rect, obs.rect):
                # Push back player (placeholder)
                player.rect.move_ip(-player.direction.x * player.speed, -player.direction.y * player.speed)
            for enemy in self.enemies:
                if rect_collision(enemy.rect, obs.rect):
                    enemy.rect.move_ip(-enemy.direction.x * enemy.speed, -enemy.direction.y * enemy.speed)

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
        # Draw bg first
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        for obs in self.obstacles:
            obs.draw(screen)  # Vẽ obs (rect xanh placeholder)
        for spawn in self.spawn_points:
            spawn.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)