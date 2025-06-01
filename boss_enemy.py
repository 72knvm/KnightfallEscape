import pygame
import random
from goblin import Goblin
from projectile import Projectile

class BossSaman(pygame.sprite.Sprite):
    def __init__(self, x, y, image, fireball_group, enemy_group, assets):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        self.health = 20
        self.speed = 1
        self.direction = 1

        self.fireball_group = fireball_group
        self.enemy_group = enemy_group
        self.assets = assets
        self.projectiles = pygame.sprite.Group()

        self.fireball_cooldown = 150
        self.fireball_timer = 0

        self.summon_cooldown = 600
        self.summon_timer = 0

    def update(self, platform_group, player):
        # Ganti arah ke arah player
        if player.rect.centerx > self.rect.centerx:
            self.direction = 1
        else:
            self.direction = -1

        # Bergerak bolak-balik seperti archer
        self.rect.x += self.speed * self.direction
        if pygame.sprite.spritecollide(self, platform_group, False):
            self.direction *= -1
            self.rect.x += self.speed * self.direction

        # Jika terlalu dekat dengan player, mundur
        dx = player.rect.centerx - self.rect.centerx
        if abs(dx) < 100:
            self.rect.x -= self.speed * self.direction

        # Fireball attack jika lihat player
        self.fireball_timer += 1
        if self.fireball_timer >= self.fireball_cooldown:
            if abs(dx) < 500 and self.direction == (1 if dx > 0 else -1):
                self.cast_fireball()
                self.fireball_timer = 0

        # Summon goblins
        self.summon_timer += 1
        if self.summon_timer >= self.summon_cooldown:
            self.summon_goblins()
            self.summon_timer = 0

        # Update peluru
        self.projectiles.update()

    def cast_fireball(self):
        fireball = Projectile(self.rect.centerx, self.rect.centery, self.direction, speed=5)
        fireball.image.fill((255, 100, 0))  # 🔥 warna merah-oranye
        self.projectiles.add(fireball)
        print("🔥 Boss Saman menembakkan fireball!")

    def summon_goblins(self):
        # 🔊 Mainkan suara summon
        if self.assets and "summon_sound" in self.assets:
            print("🔮 Memainkan suara summon.wav")
            self.assets["summon_sound"].stop()
            self.assets["summon_sound"].play()

        for _ in range(2):
            variant = random.choice(["knight", "archer"])
            x_offset = random.randint(-80, 80)
            goblin = Goblin(self.rect.centerx + x_offset, self.rect.bottom, variant=variant, assets=self.assets)
            self.enemy_group.add(goblin)
            print(f"👾 Boss summon Goblin {variant}")

    def take_damage(self, amount):
        self.health -= amount
        print(f"💥 Boss terkena {amount}, sisa: {self.health}")
        if self.health <= 0:
            print("☠️ Boss kalah!")
            self.kill()
