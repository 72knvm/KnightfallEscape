import pygame
from enemy.enemy import Enemy
from projectile import Projectile

class Goblin(Enemy):
    def __init__(self, x, y, image=None, variant="knight"):
        if image is None:
            image = pygame.Surface((40, 60))
            if variant == "knight":
                image.fill((255, 165, 0))  # oranye
            else:
                image.fill((0, 255, 255))  # cyan

        self.projectiles = pygame.sprite.Group()

        super().__init__(x, y, image)
        self.variant = variant
        if variant == "knight":
            self.health = 30
        else:
            self.health = 20

        self.speed = 1.5 if variant == "archer" else 1
        self.direction = 1  # 1 ke kanan, -1 ke kiri
        self.attack_cooldown = 60
        self.attack_timer = 0

        self.vel_y = 0
        self.gravity = 1
        self.on_ground = False

    def update(self, platform_group, player):
        # Gerak horizontal
        self.rect.x += self.speed * self.direction

        # Cek tabrakan horizontal, balik arah jika nabrak platform/tembok
        if pygame.sprite.spritecollide(self, platform_group, False):
            self.direction *= -1
            self.rect.x += self.speed * self.direction

        # Cek tepi platform agar tidak terjatuh
        if self.direction == 1:
            front_x = self.rect.right + self.speed
        else:
            front_x = self.rect.left - self.speed

        front_y = self.rect.bottom + 5
        front_rect = pygame.Rect(front_x, front_y, 2, 2)

        on_platform_ahead = False
        for platform in platform_group:
            if platform.rect.colliderect(front_rect):
                on_platform_ahead = True
                break

        if not on_platform_ahead:
            self.direction *= -1
            self.rect.x += self.speed * self.direction

        # Gravitasi dan gerak vertikal
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Deteksi tabrakan vertikal dengan platform
        self.on_ground = False
        for platform in platform_group:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        # Update peluru yang sudah ditembakkan
        self.projectiles.update()

        # Update serangan
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack(player)
            self.attack_timer = 0

    def attack(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = abs(self.rect.centery - player.rect.centery)

        if self.variant == "knight":
            if abs(dx) < 50 and dy < 40:
                print("Goblin Knight menyerang!")
                player.take_damage()

        elif self.variant == "archer":
            if abs(dx) < 300 and dy < 60:
                direction = 1 if dx > 0 else -1
                print("Goblin Archer menembak panah!")
                proj = Projectile(self.rect.centerx, self.rect.centery, direction)
                self.projectiles.add(proj)

    def take_damage(self, amount):
        self.health -= amount
        print(f"Goblin kena damage {amount}, sisa health: {self.health}")
        if self.health <= 0:
            self.kill()
            print("Goblin mati!")
