import pygame
from enemy.enemy import Enemy  # mewarisi dari Enemy → Character → GameObject

class Goblin(Enemy):
    def __init__(self, x, y, image, variant="knight"):
        super().__init__(x, y, image)
        self.variant = variant  # "knight" atau "archer"
        self.health = 50
        self.speed = 1.5 if variant == "archer" else 1
        self.direction = 1  # 1 ke kanan, -1 ke kiri
        self.attack_cooldown = 60
        self.attack_timer = 0

    def update(self, platform_group):
        # Gerakan dasar kiri-kanan
        self.rect.x += self.speed * self.direction

        # Tabrak platform atau tepi → balik arah
        if pygame.sprite.spritecollide(self, platform_group, False):
            self.direction *= -1
            self.rect.x += self.speed * self.direction

        # Timer attack
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack()
            self.attack_timer = 0

    def attack(self):
        if self.variant == "archer":
            print("Goblin Archer shoots arrow!")
            # Nanti bisa spawn peluru panah
        elif self.variant == "knight":
            print("Goblin Knight swings sword!")
            # Cek jarak ke player dan kurangi nyawa jika kena

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
