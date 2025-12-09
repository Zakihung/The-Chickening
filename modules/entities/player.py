# modules/entities/player.py
import pygame
import random
from modules.entities.base_entity import BaseEntity
from modules.utils.constants import (
    PLAYER_HP_DEFAULT, PLAYER_SPEED_DEFAULT, EGGNERGY_MAX, DODGE_COOLDOWN,
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_YELLOW, COLOR_BLACK, COLOR_RED,
    MELEE_RANGE, PLAYER_DAMAGE_DEFAULT, RANGED_RANGE, BOMB_DAMAGE, BOMB_AOE_RADIUS, BOMB_LIMIT, THOC_LOSS_ON_DEATH
)
from modules.entities.projectile import Projectile
from modules.utils.helpers import rect_collision
from modules.entities.resource import Resource

class Player(BaseEntity):
    def __init__(self, sound_manager=None):
        super().__init__(
            x=SCREEN_WIDTH // 2 - 50,
            y=SCREEN_HEIGHT // 2 - 50,
            width=100, height=100,
            hp=PLAYER_HP_DEFAULT,
            speed=PLAYER_SPEED_DEFAULT
        )
        try:
            self.image = pygame.image.load('assets/images/player/chicken.png')
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.original_image = self.image
        except pygame.error as e:
            print(f"Error loading player sprite: {e}")
            self.image = None

        self.eggnergy = EGGNERGY_MAX
        self.invincible = False
        self.dodge_speed_multiplier = 2
        self.dodge_duration = 0
        self.dodge_cooldown_timer = 0
        self.melee_cooldown = 0
        self.melee_duration = 0
        self.melee_damage = PLAYER_DAMAGE_DEFAULT
        self.melee_hitbox = None
        self.ranged_cooldown = 0
        self.ranged_cost = 10
        self.projectiles = []
        self.bomb_cooldown = 0
        self.bomb_max = BOMB_LIMIT
        self.bomb_current = self.bomb_max
        self.bomb_regen_timer = 0
        self.enemies = []
        self.thoc_collected = 0
        self.thoc_stored = 0
        self.dropped_resources = []
        self.equipped_items = []
        self.armor = 0
        self.burn_damage = 0
        self.equipped_slots = {'weapon': None, 'armor': None, 'accessory': None, 'boots': None}
        self.inventory = []
        self.base_melee_damage = PLAYER_DAMAGE_DEFAULT
        self.base_speed = PLAYER_SPEED_DEFAULT
        self.unlocked_skills = []
        self.crit_rate = 0.0
        self.branch = None
        self.armor_mult = 1.0
        self.ranged_pierce = 0
        self.bomb_aoe_radius = BOMB_AOE_RADIUS
        self.bomb_stun = 0.0
        self.upgrade_levels = {'melee': 0, 'ranged': 0, 'bomb': 0}
        self.sound_manager = sound_manager
        self.dodge_chance = 0.0
        self.chuong_level = 0
        self.regen_hp = 0
        self.shop_discount = 0.0  # Updated on upgrade
        self.mission_progress = {'kill_runner': 0, 'destroy_spawn': 0, 'collect_thoc': 0}

    def update(self, delta_time, keys):
        super().update(delta_time)

        self.direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x -= 1
            self.image = pygame.transform.flip(self.original_image, True, False)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x += 1
            self.image = self.original_image

        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        if keys[pygame.K_SPACE] and self.dodge_cooldown_timer <= 0 and self.dodge_duration <= 0:
            if self.direction.length() > 0:
                self.dodge_duration = 0.5
                self.dodge_cooldown_timer = DODGE_COOLDOWN / 1000.0
                self.invincible = True
                self.speed *= self.dodge_speed_multiplier
                if self.sound_manager:
                    self.sound_manager.play_sfx('cluck', 0.8)

        if self.dodge_duration > 0:
            self.dodge_duration -= delta_time
            if self.dodge_duration <= 0:
                self.invincible = False
                self.speed /= self.dodge_speed_multiplier
        if self.dodge_cooldown_timer > 0:
            self.dodge_cooldown_timer -= delta_time

        if keys[pygame.K_j] and self.melee_cooldown <= 0 and self.melee_duration <= 0:
            if self.direction.length() > 0:
                self.melee_duration = 0.2
                self.melee_cooldown = 0.5
                hitbox_offset = self.direction * MELEE_RANGE
                self.melee_hitbox = pygame.Rect(
                    self.rect.centerx + hitbox_offset.x - 25,
                    self.rect.centery + hitbox_offset.y - 25,
                    50, 50
                )
                if self.sound_manager:
                    self.sound_manager.play_sfx('cluck', 0.8)

        if self.melee_hitbox:
            for enemy in self.enemies:
                if rect_collision(self.melee_hitbox, enemy.rect):
                    enemy.take_damage(self.melee_damage, self.rect.center)

        if self.melee_duration > 0:
            self.melee_duration -= delta_time
            if self.melee_duration <= 0:
                self.melee_hitbox = None
        if self.melee_cooldown > 0:
            self.melee_cooldown -= delta_time

        if keys[pygame.K_k] and self.ranged_cooldown <= 0 and self.eggnergy >= self.ranged_cost:
            if self.direction.length() > 0:
                self.ranged_cooldown = 0.3
                self.eggnergy -= self.ranged_cost
                proj = Projectile(self.rect.centerx, self.rect.centery, self.direction, 'ranged', 15, 10)
                self.projectiles.append(proj)
                if self.sound_manager:
                    self.sound_manager.play_sfx('cluck', 0.8)

        if self.ranged_cooldown > 0:
            self.ranged_cooldown -= delta_time

        if keys[pygame.K_l] and self.bomb_cooldown <= 0 and self.bomb_current > 0:
            self.bomb_cooldown = 1.0
            self.bomb_current -= 1
            start_x, start_y = self.rect.center
            if self.direction.length() > 0:
                offset = self.direction.normalize() * 50
                start_x += offset.x
                start_y += offset.y
            proj = Projectile(start_x, start_y, self.direction, 'bomb', BOMB_DAMAGE, 5, BOMB_AOE_RADIUS)
            self.projectiles.append(proj)
            if self.sound_manager:
                self.sound_manager.play_sfx('cluck', 0.8)

        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= delta_time

        for proj in self.projectiles[:]:
            proj.update(delta_time)
            proj.check_collision(self.enemies)
            if not proj.alive:
                self.projectiles.remove(proj)

        self.bomb_regen_timer += delta_time
        if self.bomb_regen_timer >= 10 and self.bomb_current < self.bomb_max:
            self.bomb_current += 1
            self.bomb_regen_timer = 0

        self.eggnergy = min(self.eggnergy + 10 * delta_time, EGGNERGY_MAX)

        if self.hp <= 0 and self.alive:
            self.alive = False
            self.die()
            if self.sound_manager:
                self.sound_manager.play_sfx('auu', 0.8)

    def take_damage(self, damage, attacker_pos=None):
        if random.random() < self.dodge_chance:
            return
        damage /= self.armor_mult
        super().take_damage(damage)

    def draw(self, screen):
        if self.image and self.invincible:
            tint_surface = self.image.copy()
            tint_surface.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(tint_surface, self.rect.topleft)
        else:
            super().draw(screen)

        if self.melee_hitbox:
            pygame.draw.rect(screen, COLOR_RED, self.melee_hitbox, 2)

        for proj in self.projectiles:
            proj.draw(screen)

        energy_ratio = self.eggnergy / EGGNERGY_MAX
        bar_width = self.rect.width * energy_ratio
        energy_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, 5)
        pygame.draw.rect(screen, COLOR_YELLOW, energy_bar_rect)
        full_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 20, self.rect.width, 5)
        pygame.draw.rect(screen, COLOR_BLACK, full_bar_rect, 1)

    def store_thoc(self):
        self.thoc_stored += self.thoc_collected
        self.thoc_collected = 0

    def die(self):
        if self.thoc_collected > 0:
            lost = int(self.thoc_collected * THOC_LOSS_ON_DEATH)
            remaining = self.thoc_collected - lost
            self.thoc_collected = 0
            for _ in range(remaining // 5):
                drop_x = self.rect.centerx + random.randint(-50, 50)
                drop_y = self.rect.centery + random.randint(-50, 50)
                drop = Resource(drop_x, drop_y, 5)
                self.dropped_resources.append(drop)
            print(f"Lost {lost} thóc! Dropped {remaining} to collect again.")
        self.hp = self.max_hp
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.alive = True