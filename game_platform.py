import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, spawnable=True, image=None):
        super().__init__()
        if image:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            tile_width, tile_height = image.get_size()

            # Ulang gambar tile sepanjang width dan tinggi platform
            for i in range(0, width, tile_width):
                for j in range(0, height, tile_height):
                    self.image.blit(image, (i, j))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((169, 169, 169))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawnable = spawnable

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, image_dict=None):
        super().__init__()
        self.type = item_type
        self.collected = False

        # Gambar item
        if image_dict and item_type in image_dict:
            self.image = image_dict[item_type]
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0) if item_type == 'health' else (0, 0, 255))

        # Posisi berdasarkan gambar
        self.rect = self.image.get_rect(topleft=(x, y))

class AnimatedPortal(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, frame_duration=100, render_offset_x=0, render_offset_y=0):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = frame_duration
        self.image = self.frames[0]
        self.render_offset_x = render_offset_x
        self.render_offset_y = render_offset_y
        self.rect = self.image.get_rect(topleft=(x, y + render_offset_y))  # tetap logika collision

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now
