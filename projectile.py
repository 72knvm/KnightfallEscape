import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=4, image=None):
        super().__init__()
        if image is not None:
            self.image = image.copy()
        else:
            self.image = pygame.Surface((10, 5))
            self.image.fill((255, 255, 0))

        self.direction = direction
        self.speed = speed

        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.speed * self.direction
        print(f"🚀 Panah bergerak ke {self.rect.x}")
        if self.rect.right < 0 or self.rect.left > 1600:  # atau batas layar
            self.kill()
