import pygame

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, frames, speed=4):
        super().__init__()
        self.frames = frames
        self.direction = direction
        self.speed = speed

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 5  # update frame setiap 5 tick

        # Gambar awal
        self.image = self.frames[0] if direction == 1 else pygame.transform.flip(self.frames[0], True, False)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Gerakkan fireball
        self.rect.x += self.speed * self.direction

        # Update animasi
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            frame = self.frames[self.frame_index]
            self.image = frame if self.direction == 1 else pygame.transform.flip(frame, True, False)

        # Hapus jika keluar layar
        if self.rect.right < 0 or self.rect.left > 1600:
            self.kill()
