import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((169, 169, 169))  # Warna abu-abu
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Perhatikan jika perlu mengatur pergerakan platform atau logika interaksi player
        pass

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.type = item_type
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))

        if item_type == 'life':
            self.image.fill((0, 255, 0))
        elif item_type == 'shield':
            self.image.fill((0, 0, 255))
        elif item_type == 'fireball':
            self.image.fill((255, 0, 0))
        elif item_type == 'portal':
            self.image.fill((255, 255, 0))
        else:
            self.image.fill((150, 150, 150))