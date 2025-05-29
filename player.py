import pygame

def find_spawn_y(platforms, spawn_x, player_height):
    candidates = [p for p in platforms if p.rect.left <= spawn_x <= p.rect.right]
    if not candidates:
        return 400
    highest = min(candidates, key=lambda p: p.rect.top)
    return highest.rect.top - player_height

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, enemies, idle_frames, walk_right_frames, walk_left_frames, jump_frames, attack_frames, hurt_frames, platforms=None):
        super().__init__()
        self.idle_frames = idle_frames
        self.walk_right_frames = walk_right_frames
        self.walk_left_frames = walk_left_frames
        self.jump_frames = jump_frames
        self.attack_frames = attack_frames
        self.hurt_frames = hurt_frames

        self.frame_index = 0
        self.current_frames = self.idle_frames
        self.image = self.current_frames[self.frame_index]
        self.rect = self.image.get_rect()

        self.animation_speed = 0.1
        self.frame_timer = 0

        self.vel_y = 0
        self.jump_power = -15
        self.speed = 5
        self.gravity = 1
        self.on_ground = False

        self.lives = 3
        self.damage_cooldown = 1000
        self.last_damage_time = 0
        self.is_invulnerable = False

        self.attacking = False
        self.attack_frame_index = 0
        self.attack_frame_timer = 0
        self.attack_animation_speed = 0.1
        self.attack_cooldown = 500
        self.last_attack_time = 0

        self.is_game_over = False
        self.enemies = enemies
        self.is_running = False
        self.facing_right = True

        self.death_frames = []
        self.death_frame_index = 0
        self.death_frame_timer = 0
        self.death_animation_speed = 0.12
        self.playing_death = False

        self.attack_hitbox = pygame.Rect(0, 0, 50, 50)
        self.has_dealt_damage = False
        self.debug_hitbox = False

        self.is_hurt = False
        self.hurt_start_time = 0
        self.hurt_frame_index = 0
        self.hurt_frame_timer = 0
        self.hurt_animation_speed = 0.1
        self.hurt_duration = 300

        self.parrying = False
        self.parry_start_time = 0
        self.parry_duration = 600
        self.parry_frames = []
        self.parry_frame_index = 0
        self.parry_frame_timer = 0
        self.parry_animation_speed = 0.1

        self.reset(x, y, platforms)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        if self.debug_hitbox and self.attacking:
            adjusted_hitbox = self.attack_hitbox.move(-camera_x, -camera_y)
            pygame.draw.rect(surface, (255, 0, 0), adjusted_hitbox, 2)

    def deal_damage(self):
        hitbox_width = 50
        hitbox_height = 50
        vertical_offset = 70
        if self.facing_right:
            self.attack_hitbox = pygame.Rect(self.rect.right - 70, self.rect.top + vertical_offset, hitbox_width, hitbox_height)
        else:
            self.attack_hitbox = pygame.Rect(self.rect.left - hitbox_width + 70, self.rect.top + vertical_offset, hitbox_width, hitbox_height)

        for enemy in self.enemies:
            if self.attack_hitbox.colliderect(enemy.rect):
                if hasattr(enemy, "take_damage"):
                    enemy.take_damage(1)
                    print("🎯 Musuh terkena hit!")

    def update_attack_animation(self, dt):
        self.attack_frame_timer += dt
        if self.attack_frame_timer >= self.attack_animation_speed:
            self.attack_frame_timer = 0
            self.attack_frame_index += 1

            if self.attack_frame_index < len(self.attack_frames):
                center = self.rect.center
                frame = self.attack_frames[self.attack_frame_index]
                self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)
                self.rect = self.image.get_rect()
                self.rect.center = center

                if self.attack_frame_index in [1, 2] and not self.has_dealt_damage:
                    self.deal_damage()
                    self.has_dealt_damage = True
            else:
                self.attacking = False
                self.attack_frame_index = 0
                self.current_frames = self.walk_right_frames if self.facing_right else self.walk_left_frames
                self.frame_index = 0
                self.frame_timer = 0
                self.image = self.current_frames[self.frame_index]
                self.has_dealt_damage = False

    def play_death_animation(self, dt):
        if self.death_frame_index < len(self.death_frames):
            self.death_frame_timer += dt
            if self.death_frame_timer >= self.death_animation_speed:
                self.death_frame_timer = 0
                frame = self.death_frames[self.death_frame_index]
                self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)
                self.death_frame_index += 1
        else:
            print("💀 Death animation finished.")
            self.playing_death = False

    def update(self, platforms, keys, dt):
        current_time = pygame.time.get_ticks()

        if self.playing_death:
            self.play_death_animation(dt)
            return

        if keys[pygame.K_r] and not self.parrying and not self.attacking and not self.is_hurt:
            self.parrying = True
            self.parry_start_time = current_time
            self.parry_frame_index = 0
            self.parry_frame_timer = 0
            if self.parry_frames:
                self.image = self.parry_frames[0] if self.facing_right else pygame.transform.flip(self.parry_frames[0], True, False)

        if self.parrying:
            self.parry_frame_timer += dt
            if self.parry_frames and self.parry_frame_timer >= self.parry_animation_speed:
                self.parry_frame_timer = 0
                self.parry_frame_index = (self.parry_frame_index + 1) % len(self.parry_frames)
                frame = self.parry_frames[self.parry_frame_index]
                self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)

            if current_time - self.parry_start_time > self.parry_duration:
                self.parrying = False

            return

        if self.is_hurt:
            self.hurt_frame_timer += dt
            if self.hurt_frame_timer >= self.hurt_animation_speed:
                self.hurt_frame_timer = 0
                self.hurt_frame_index = (self.hurt_frame_index + 1) % len(self.hurt_frames)
                frame = self.hurt_frames[self.hurt_frame_index]
                self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)

            if current_time - self.hurt_start_time > self.hurt_duration:
                self.is_hurt = False
            return

        if self.is_game_over:
            return

        if self.attacking:
            self.update_attack_animation(dt)
            return

        if keys[pygame.K_a]:
            self.collision_rect.x -= self.speed
            self.handle_horizontal_collision(platforms)
            self.is_running = True
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.collision_rect.x += self.speed
            self.handle_horizontal_collision(platforms)
            self.is_running = True
            self.facing_right = True
        else:
            if self.is_running:
                self.frame_index = 0
            self.is_running = False

        if not self.on_ground:
            new_frames = [pygame.transform.flip(f, True, False) for f in self.jump_frames] if not self.facing_right else self.jump_frames
        else:
            if self.is_running:
                new_frames = self.walk_right_frames if self.facing_right else self.walk_left_frames
            else:
                new_frames = self.idle_frames if self.facing_right else [pygame.transform.flip(f, True, False) for f in self.idle_frames]

        if self.current_frames != new_frames:
            self.current_frames = new_frames
            self.frame_index = 0
            self.frame_timer = 0

        self.frame_timer += dt
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.frame_index]

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        self.vel_y += self.gravity
        self.collision_rect.y += self.vel_y
        self.handle_vertical_collision(platforms)
        self.rect.midbottom = self.collision_rect.midbottom
        self.rect.y += 45

        if keys[pygame.K_f]:
            if not self.attacking and current_time - self.last_attack_time >= self.attack_cooldown:
                self.attacking = True
                self.attack_frame_index = 0
                self.attack_frame_timer = 0
                frame = self.attack_frames[0]
                self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)
                self.last_attack_time = current_time
                self.has_dealt_damage = False

    def take_damage(self, damage=1):
        current_time = pygame.time.get_ticks()

        if self.is_invulnerable:
            print("⚠️ Player sedang invulnerable. Damage diabaikan.")
            return

        if current_time - self.last_damage_time >= self.damage_cooldown:
            self.lives -= damage
            self.last_damage_time = current_time

            if self.lives > 0:
                self.is_hurt = True
                self.hurt_start_time = current_time
                self.hurt_frame_index = 0
                self.hurt_frame_timer = 0
                frame = self.hurt_frames[0]
                self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)
                print(f"💢 Player terkena damage! Nyawa tersisa: {self.lives}")
            else:
                print("💀 Player mati! Memainkan animasi death...")
                self.is_invulnerable = True
                self.playing_death = True
                self.death_frame_index = 0
                self.death_frame_timer = 0
                self.image = self.death_frames[0] if self.facing_right else pygame.transform.flip(self.death_frames[0], True, False)
                self.is_game_over = True

    def reset(self, x=100, y=None, platforms=None):
        collision_width = 50
        collision_height = 50
        player_height = collision_height

        if y is None:
            y = find_spawn_y(platforms, x, player_height) if platforms else 400

        self.rect.topleft = (x, y)
        collision_x = x + (self.rect.width - collision_width) // 2
        collision_y = y + self.rect.height - collision_height
        self.collision_rect = pygame.Rect(collision_x, collision_y, collision_width, collision_height)

        self.lives = 3
        self.is_game_over = False
        self.is_invulnerable = False
        self.last_damage_time = 0
        self.vel_y = 0  # ⬅️ Harus di-set sebelum handle_vertical_collision
        self.attacking = False
        self.last_attack_time = 0
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.is_hurt = False
        self.hurt_frame_index = 0
        self.hurt_frame_timer = 0
        self.parrying = False
        self.playing_death = False
        self.death_frame_index = 0
        self.death_frame_timer = 0

        # ✅ Deteksi apakah langsung di atas platform
        if platforms is not None:
            self.handle_vertical_collision(platforms)

    def handle_horizontal_collision(self, platforms):
        for platform in platforms:
            if self.collision_rect.colliderect(platform.rect):
                if self.collision_rect.centerx < platform.rect.centerx:
                    self.collision_rect.right = platform.rect.left
                else:
                    self.collision_rect.left = platform.rect.right

    def handle_vertical_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.collision_rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.collision_rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.collision_rect.top = platform.rect.bottom
                    self.vel_y = 0
