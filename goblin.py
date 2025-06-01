import pygame
from enemy.enemy import Enemy
from projectile import Projectile

class Goblin(Enemy):
    def __init__(self, x, y, image=None, variant="knight", assets=None):
        if image is None:
            image = pygame.Surface((40, 60), pygame.SRCALPHA)

        super().__init__(x, y, image)

        self.variant = variant
        self.projectiles = pygame.sprite.Group()
        self.health = 3 if variant == "knight" else 2
        self.speed = 1 if variant == "knight" else 1.5
        self.direction = 1
        self.vel_y = 0
        self.gravity = 1
        self.on_ground = False
        self.attack_timer = 0
        self.moving = True
        self.assets = assets
        self.state = "idle"
        self.post_attack_timer = 0
        self.post_attack_delay = 30

        self.animation_frames = {}
        self.current_animation = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.animation_speed = 0.15
        self.facing_right = True
        self.has_shot = False
        self.target_player = None

        self.dead = False
        self.death_wait_timer = 0
        self.death_wait_duration = 60

        if assets is not None:
            if self.variant == "archer":
                self.animation_frames = assets.get("archer", {})
            elif self.variant == "knight":
                self.animation_frames = assets.get("goblin_knight", {})

            if "idle" in self.animation_frames:
                self.image = self.animation_frames["idle"][0]
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self, platform_group, player):
        if self.dead:
            self.update_animation()
            return

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance_x = abs(dx)

        self.facing_right = dx > 0

        # Saat animasi attack sedang berjalan, hentikan gerakan
        if self.current_animation == "attack":
            self.moving = False

        if self.variant == "archer":
            if self.state == "post_attack_idle":
                self.speed = 0
                self.moving = False
                if self.current_animation != "idle":
                    self.current_animation = "idle"
                    self.frame_index = 0
                self.post_attack_timer += 1
                if self.post_attack_timer >= self.post_attack_delay:
                    self.state = "walk"
                    self.post_attack_timer = 0

            elif self.state == "attack":
                self.speed = 0
                self.moving = False
                if self.current_animation != "attack":
                    self.current_animation = "attack"
                    self.frame_index = 0

            elif distance_x < 250:
                self.state = "walk"
                self.speed = 1.5
                self.moving = True
                self.direction = 1 if dx > 0 else -1
                if self.current_animation != "walk":
                    self.current_animation = "walk"
                    self.frame_index = 0
            else:
                self.state = "idle"
                self.speed = 0
                self.moving = False
                if self.current_animation != "idle":
                    self.current_animation = "idle"
                    self.frame_index = 0

        elif self.variant == "knight":
            if distance_x < 250 and self.current_animation != "attack":
                self.moving = True
                self.direction = 1 if dx > 0 else -1
                if self.current_animation != "walk":
                    self.current_animation = "walk"
                    self.frame_index = 0
            elif self.current_animation != "attack":
                self.moving = False
                if self.current_animation != "idle":
                    self.current_animation = "idle"
                    self.frame_index = 0

        if self.moving:
            self.rect.x += self.speed * self.direction

        if pygame.sprite.spritecollide(self, platform_group, False):
            self.direction *= -1
            if self.moving:
                self.rect.x += self.speed * self.direction

        front_x = self.rect.right + self.speed if self.direction == 1 else self.rect.left - self.speed
        front_y = self.rect.bottom + 5
        front_rect = pygame.Rect(front_x, front_y, 2, 2)
        if not any(p.rect.colliderect(front_rect) for p in platform_group):
            self.direction *= -1
            if self.moving:
                self.rect.x += self.speed * self.direction

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in platform_group:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        self.projectiles.update()
        self.attack_timer += 1
        if self.attack_timer >= 60:
            self.attack(player)
            self.attack_timer = 0

        self.update_animation()

    def update_animation(self):
        if not self.animation_frames or self.current_animation not in self.animation_frames:
            return

        frames = self.animation_frames[self.current_animation]
        total_frames = len(frames)

        if self.frame_index >= total_frames:
            self.frame_index = 0

        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            if not self.dead or self.current_animation != "dead":
                self.frame_index = (self.frame_index + 1) % total_frames
            else:
                self.frame_index = min(self.frame_index + 1, total_frames - 1)

        # Flip DULU
        raw_frame = frames[self.frame_index]
        flipped = raw_frame if self.facing_right else pygame.transform.flip(raw_frame, True, False)

        # Baru TRIM setelah flip
        trimmed_rect = flipped.get_bounding_rect()
        frame = flipped.subsurface(trimmed_rect).copy()

        # Scale (hanya knight)
        if self.variant == "knight":
            scale_ratio = 1.0
            size = frame.get_size()
            frame = pygame.transform.scale(frame, (int(size[0] * scale_ratio), int(size[1] * scale_ratio)))

        # Jaga posisi agar tidak bergeser
        prev_bottomleft = self.rect.bottomleft
        self.image = frame
        self.rect = self.image.get_rect()
        self.rect.bottomleft = prev_bottomleft

        # Setelah attack selesai → kembali idle
        if self.variant == "knight" and self.current_animation == "attack" and self.frame_index == total_frames - 1:
            self.moving = True
            self.current_animation = "idle"
            self.frame_index = 0

        if self.dead and self.current_animation == "dead" and self.frame_index == total_frames - 1:
            self.death_wait_timer += 1
            if self.death_wait_timer >= self.death_wait_duration:
                self.kill()

        if self.variant == "archer":
            if self.current_animation == "attack" and self.frame_index == 0:
                self.has_shot = False
                
            if self.current_animation == "attack" and self.frame_index == 9 and not self.has_shot:
                direction = 1 if self.facing_right else -1
                offset_x = 40 if self.facing_right else -40
                offset_y = 40
                proj_x = self.rect.centerx + offset_x
                proj_y = self.rect.top + offset_y

                # 🔊 Mainkan suara arrow saat tembakan dilakukan
                if self.assets and "arrow_sound" in self.assets:
                    self.assets["arrow_sound"].stop()
                    self.assets["arrow_sound"].play()

                proj = Projectile(proj_x, proj_y, direction, image=self.assets.get("arrow"))
                self.projectiles.add(proj)
                print("🏹 Panah ditembakkan di frame ke-10!")
                self.has_shot = True
                self.state = "post_attack_idle"

    def attack(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        if self.variant == "knight":
            if abs(dx) < 50 and abs(dy) < 40:
                print("🗡️ Goblin Knight menyerang!")
                if self.current_animation != "attack":
                    self.current_animation = "attack"
                    self.frame_index = 0
                    if self.assets and "slash_goblin_sound" in self.assets:
                        print("🔊 Memainkan slash_goblin_sound dari attack()")
                        self.assets["slash_goblin_sound"].stop()
                        self.assets["slash_goblin_sound"].play()
                self.moving = False
                if hasattr(player, "take_damage"):
                    player.take_damage(1)

        elif self.variant == "archer":
            if abs(dx) < 300 and self.state != "attack":
                print("🏹 Goblin Archer bersiap menembak panah!")
                self.state = "attack"
                self.current_animation = "attack"
                self.frame_index = 0
                self.has_shot = False
                self.moving = False
                self.target_player = player

    def take_damage(self, amount):
        self.health -= amount
        print(f"Goblin ({self.variant}) kena damage {amount}, sisa: {self.health}")

        # 🔊 Mainkan suara goblin kena hit
        if self.assets and "hit_goblin_sound" in self.assets:
            self.assets["hit_goblin_sound"].stop()
            self.assets["hit_goblin_sound"].play()

        if self.health <= 0:
            if self.current_animation != "dead":
                self.current_animation = "dead"
                self.frame_index = 0

                # 🔊 (opsional) mainkan suara mati (jika beda dari suara hit)
                if self.assets and "goblin_death_sound" in self.assets:
                    self.assets["goblin_death_sound"].stop()
                    self.assets["goblin_death_sound"].play()

            self.dead = True
            print("☠️ Goblin mati (menunggu animasi dan delay)")

        else:
            if "hurt" in self.animation_frames:
                self.current_animation = "hurt"
                self.frame_index = 0
            else:
                print("⚠️ Animasi hurt tidak ditemukan")
