import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=7):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 0))  # warna kuning
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction  # 1 kanan, -1 kiri
        self.speed = speed

    def update(self):
        self.rect.x += self.speed * self.direction
        # Bisa tambah cek apakah projectile keluar layar, lalu kill()
