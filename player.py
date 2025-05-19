import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, enemies):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))  # warna merah
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.jump_power = -15
        self.speed = 5
        self.gravity = 1
        self.on_ground = False

        # Sistem nyawa
        self.lives = 3

        # Sistem Damage cooldown
        self.damage_cooldown = 1000  # milidetik cooldown antar damage
        self.last_damage_time = 0  # mulai dari 0 supaya damage bisa diterima langsung

        # Basic attack
        self.attacking = False
        self.attack_cooldown = 500  # milidetik
        self.last_attack_time = 0

        self.is_game_over = False

        # Simpan grup musuh agar bisa serang
        self.enemies = enemies

    def update(self, platforms, keys):
        if self.is_game_over:
            return  # Tidak bisa bergerak kalau game over

        # Gerakan kiri/kanan
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        # Lompat
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        # Gravitasi
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Deteksi tabrakan dengan platform
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        # Basic attack dengan cooldown
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_f]:
            if not self.attacking and current_time - self.last_attack_time >= self.attack_cooldown:
                self.basic_attack()
                self.last_attack_time = current_time

    def basic_attack(self):
        self.attacking = True
        print("Player melakukan basic attack!")

        for enemy in self.enemies:
            distance = abs(enemy.rect.centerx - self.rect.centerx)
            if distance < 50:  # batas jarak serang
                enemy.take_damage(10)  # berikan damage 10

        self.attacking = False

    def take_damage(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time < self.damage_cooldown:
            return  # masih cooldown, ignore damage

        self.lives = max(self.lives - 1, 0)
        self.last_damage_time = current_time
        print(f"Player kena damage! Nyawa tersisa: {self.lives}")

        if self.lives <= 0:
            self.is_game_over = True
            print("GAME OVER! Player kehilangan semua nyawa.")

    def reset(self, x=100, y=400):
        # Reset posisi dan status player untuk ulangi level
        self.rect.topleft = (x, y)
        self.lives = 3
        self.is_game_over = False
        self.last_damage_time = 0
        self.vel_y = 0
        self.on_ground = False
        self.attacking = False
        self.last_attack_time = 0
