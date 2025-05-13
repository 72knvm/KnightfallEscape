import pygame
import random
from enemy.boss_enemy import BossEnemy
from enemy.goblin import Goblin
from enemy.fireball import Fireball  # fireball bisa dibuat terpisah sebagai peluru

class BossSaman(BossEnemy):
    def __init__(self, x, y, image, fireball_group, goblin_group):
        super().__init__(x, y, image)
        self.health = 200
        self.speed = 2
        self.direction = 1

        self.fireball_group = fireball_group
        self.goblin_group = goblin_group

        self.fireball_cooldown = 120
        self.fireball_timer = 0

        self.summon_cooldown = 300
        self.summon_timer = 0

    def update(self, platform_group):
        # Gerakan dasar (kiri-kanan)
        self.rect.x += self.speed * self.direction

        # Deteksi tabrakan dengan platform → ganti arah
        if pygame.sprite.spritecollide(self, platform_group, False):
            self.direction *= -1
            self.rect.x += self.speed * self.direction

        # Fireball attack
        self.fireball_timer += 1
        if self.fireball_timer >= self.fireball_cooldown:
            self.special_skill()  # fireball
            self.fireball_timer = 0

        # Summon goblin
        self.summon_timer += 1
        if self.summon_timer >= self.summon_cooldown:
            self.summon_goblins()
            self.summon_timer = 0

    def special_skill(self):
        fireball = Fireball(self.rect.centerx, self.rect.centery, self.direction)
        self.fireball_group.add(fireball)

    def summon_goblins(self):
        count = random.randint(1, 3)
        for _ in range(count):
            x_offset = random.randint(-50, 50)
            goblin = Goblin(self.rect.centerx + x_offset, self.rect.bottom)
            self.goblin_group.add(goblin)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
