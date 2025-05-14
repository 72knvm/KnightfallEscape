import pygame
from pygame.locals import *
from src.asset_loader import load_image
from src.item import Fireball

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = load_image("player_idle.png")
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.jump_power = -15
        self.speed = 5
        self.gravity = 0.8
        self.on_ground = False

        self.health = 3
        self.max_health = 5
        self.score = 0

        # Power-up
        self.has_fireball = False
        self.has_shield = False
        self.fireballs = pygame.sprite.Group()

        # Cooldown
        self.attack_cooldown = 500  # ms
        self.last_attack_time = pygame.time.get_ticks()

    def handle_input(self, keys):
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
        if keys[K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
        if keys[K_f]:
            self.attack()

    def attack(self):
        now = pygame.time.get_ticks()
        if self.has_fireball and now - self.last_attack_time >= self.attack_cooldown:
            fireball = Fireball(self.rect.centerx, self.rect.centery, direction=1)
            self.fireballs.add(fireball)
            self.last_attack_time = now

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def check_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

    def update(self, platforms, keys):
        self.handle_input(keys)
        self.apply_gravity()
        self.check_collision(platforms)
        self.fireballs.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.fireballs.draw(surface)

    def collect_item(self, item):
        if item.type == "health":
            self.health = min(self.max_health, self.health + 1)
        elif item.type == "fireball":
            self.has_fireball = True
        elif item.type == "shield":
            self.has_shield = True