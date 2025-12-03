# modules/managers/level_manager.py
import json
import math
import random
import os
import pygame
from modules.entities.base_entity import BaseEntity
from modules.entities.enemy import Enemy
from modules.utils.constants import WAVE_COUNT_PER_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_PATH, COLOR_GREEN
from modules.utils.helpers import rect_collision
from modules.entities.boss import Boss

class LevelManager:
    def __init__(self, sound_manager=None):
        with open('data/levels.json', 'r', encoding="utf8") as f:
            self.levels_data = json.load(f)['levels']
        self.current_level = 0
        self.current_wave = 0
        self.enemies = []
        self.spawn_points = []
        self.obstacles = []
        self.wave_timer = 0
        self.max_levels = len(self.levels_data)
        self.is_boss_level = False
        self.background_image = None
        self.sound_manager = sound_manager
        self.load_level(self.current_level)

    def load_level(self, level_id):
        level = next((l for l in self.levels_data if l['id'] == level_id + 1), None)
        if level:
            self.map_type = level['map_type']
            self.background = level['background']
            bg_path = os.path.join(IMAGES_PATH, 'backgrounds', self.background)
            if os.path.exists(bg_path):
                self.background_image = pygame.image.load(bg_path)
                self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            else:
                self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.background_image.fill(COLOR_GREEN)  # Fallback

            self.obstacles.clear()
            if self.map_type == 'farm':
                for _ in range(5):
                    obs = BaseEntity(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 50, 50, hp=20)
                    self.obstacles.append(obs)
            elif self.map_type == 'forest':
                for _ in range(10):
                    obs = BaseEntity(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 30, 30, hp=10)
                    self.obstacles.append(obs)
            # Add more for other types

            self.waves = level['waves'] if not self.is_boss_level else []
            self.spawn_points = [BaseEntity(sp['x'], sp['y'], 40, 40, hp=sp['hp']) for sp in level['spawn_points']]
            self.boss_data = level['boss']
            self.current_wave = 0
            self.enemies.clear()
            if self.is_boss_level and self.boss_data:
                boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.boss_data['type'], self.sound_manager)
                self.enemies.append(boss)

    def next_level(self):
        self.current_level += 1
        self.is_boss_level = (self.current_level % 5 == 0)
        if self.sound_manager:
            self.sound_manager.stop_music()
            self.sound_manager.play_music('music_wave.mp3')
        if self.current_level < self.max_levels:
            self.load_level(self.current_level)
        else:
            print("All levels cleared!")

    def update(self, delta_time, player):
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

        for obs in self.obstacles:
            if rect_collision(player.rect, obs.rect):
                player.rect.move_ip(-player.direction.x * player.speed, -player.direction.y * player.speed)
            for enemy in self.enemies:
                if rect_collision(enemy.rect, obs.rect):
                    enemy.rect.move_ip(-enemy.direction.x * enemy.speed, -enemy.direction.y * enemy.speed)

        self.wave_timer -= delta_time
        if self.wave_timer <= 0 and self.current_wave < len(self.waves) and self.spawn_points:
            wave = self.waves[self.current_wave]
            for enemy_data in wave['enemies']:
                for _ in range(enemy_data['count']):
                    spawn = random.choice(self.spawn_points)
                    enemy = Enemy(spawn.rect.centerx, spawn.rect.centery, enemy_data['type'], self.sound_manager)
                    self.enemies.append(enemy)
            self.current_wave += 1
            self.wave_timer = 5.0

        for enemy in self.enemies[:]:
            enemy.update(delta_time, player)
            if not enemy.alive:
                self.enemies.remove(enemy)

        for spawn in self.spawn_points[:]:
            if player.melee_hitbox and rect_collision(spawn.rect, player.melee_hitbox):
                spawn.take_damage(player.melee_damage)
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

        if len(self.enemies) == 0 and len(self.spawn_points) == 0 and self.current_wave >= len(self.waves):
            if self.is_boss_level:
                if all(not e.alive for e in self.enemies if isinstance(e, Boss)):
                    self.next_level()
            else:
                self.next_level()

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        for obs in self.obstacles:
            obs.draw(screen)
        for spawn in self.spawn_points:
            spawn.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)