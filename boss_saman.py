import pygame
import random
from goblin import Goblin
from fireball import Fireball

class BossSaman(pygame.sprite.Sprite):
    def __init__(self, x, y, fireball_group, enemy_group, assets):
        super().__init__()
        self.assets = assets
        self.animations = assets["shaman"]
        self.state = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8

        frame = self.animations[self.state][self.frame_index]
        self.image = frame
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_bounding_rect()
        self.rect.topleft = (x, y)

        self.health = 20
        self.speed = 1
        self.direction = 1

        self.fireball_group = fireball_group
        self.enemy_group = enemy_group
        self.projectiles = pygame.sprite.Group()

        self.fireball_cooldown = 150
        self.fireball_timer = 0

        self.summon_cooldown = 1200
        self.summon_timer = 0

        # Fisika
        self.jump_power = -15
        self.gravity = 0.8
        self.vel_y = 0
        self.on_ground = False

        self.alive = True

    def update(self, platform_group, player):
        if not self.alive:
            self.state = "death"
            self.animate()
            return

        dx = player.rect.centerx - self.rect.centerx
        self.direction = 1 if dx > 0 else -1

        # Bergerak ke arah player
        if 100 < abs(dx) < 500:
            self.state = "move"
            self.rect.x += self.speed * self.direction
            if pygame.sprite.spritecollide(self, platform_group, False):
                self.direction *= -1
                self.rect.x += self.speed * self.direction
        elif abs(dx) < 100:
            self.state = "idle"
            self.rect.x -= self.speed * self.direction
        else:
            self.state = "idle"

        # Lompat jika player di atas
        if player.rect.bottom < self.rect.top and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        # Gravitasi
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Tembak fireball
        self.fireball_timer += 1
        if self.fireball_timer >= self.fireball_cooldown:
            if abs(dx) < 500 and self.direction == (1 if dx > 0 else -1):
                self.cast_fireball()
                self.fireball_timer = 0
                self.state = "attack"

        # Summon goblin
        self.summon_timer += 1
        if self.summon_timer >= self.summon_cooldown:
            self.summon_goblins()
            self.summon_timer = 0
            self.state = "attack"

        self.animate()
        self.projectiles.update()

    def animate(self):
        frames = self.animations.get(self.state, self.animations["idle"])
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        frame = frames[self.frame_index]

        # Visual offset agar sprite tidak menggantung
        offset_y = 10
        visual_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
        visual_surface.blit(frame, (0, offset_y))

        if self.direction == -1:
            visual_surface = pygame.transform.flip(visual_surface, True, False)

        trimmed_rect = visual_surface.get_bounding_rect()
        trimmed_image = visual_surface.subsurface(trimmed_rect).copy()
        self.image = trimmed_image

        self.mask = pygame.mask.from_surface(self.image)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def cast_fireball(self):
        frames = self.assets.get("boss_fireball", [])
        if not frames:
            print("❌ Fireball frames kosong!")
            return

        # 🔊 Mainkan suara fireball
        if self.assets and "fireball_sound" in self.assets:
            print("🔥 Memainkan suara fireball")
            self.assets["fireball_sound"].stop()
            self.assets["fireball_sound"].play()

        fireball = Fireball(self.rect.centerx, self.rect.centery, self.direction, frames, speed=4)
        self.projectiles.add(fireball)

    def summon_goblins(self):
        for _ in range(2):
            variant = random.choice(["knight", "archer"])
            x_offset = random.randint(-80, 80)
            goblin = Goblin(self.rect.centerx + x_offset, self.rect.bottom, variant=variant, assets=self.assets)
            self.enemy_group.add(goblin)
            print(f"👾 Boss summon Goblin {variant}")

    def take_damage(self, amount):
        self.health -= amount
        print(f"💥 Boss terkena {amount}, sisa: {self.health}")

        # Tambahkan sound hit seperti Goblin
        if self.assets and "hit_goblin_sound" in self.assets:
            self.assets["hit_goblin_sound"].stop()
            self.assets["hit_goblin_sound"].play()

        if self.health <= 0:
            print("☠️ Boss kalah!")
            self.alive = False
            self.frame_index = 0
            self.animation_timer = 0
