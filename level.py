import pygame
from platform import Platform, Item
import random
from goblin import Goblin

class SimplePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((169, 169, 169))  # Warna abu-abu untuk platform
        self.rect = self.image.get_rect(topleft=(x, y))

MAX_LEVEL_WIDTH = 20000  # pastikan ini nilai level kamu sesuai

class Level:
    def __init__(self, level_number, player):
        self.level_number = level_number
        self.player = player  # Simpan objek player yang diterima
        self.platforms = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boss = None

        self.state = self._get_state_from_level()
        self.build_level()

    def _get_state_from_level(self):
        if 1 <= self.level_number <= 5:
            return "underground"
        elif 6 <= self.level_number <= 10:
            return "castle"
        elif 11 <= self.level_number <= 15:
            return "outside"
        return "unknown"

    def find_platform_y(self, x_pos):
            for platform in self.platforms:
                if platform.rect.left <= x_pos <= platform.rect.right:
                    return platform.rect.top
            return 550  # fallback ke tanah jika tidak ketemu

    def spawn_goblin(self, x, variant):
        # Batasi posisi spawn agar valid dan di dalam level
        if x < 0 or x > MAX_LEVEL_WIDTH:
            print(f"[WARNING] Goblin spawn di luar batas level: x={x}")
            return

        y = self.find_platform_y(x) - 60  # tinggi Goblin

        goblin = Goblin(x, y, pygame.Surface((40, 60)), variant=variant)
        color = (255, 165, 0) if variant == "knight" else (0, 255, 255)
        goblin.image.fill(color)
        self.enemies.add(goblin)

    def spawn_random_goblins(self, count=5):
        self.enemies.empty()

        platform_list = [p for p in self.platforms if getattr(p, "spawnable", True)]

        if not platform_list:
            print("[WARNING] Tidak ada platform valid untuk spawn Goblin.")
            return

        knight_count = count // 2
        archer_count = count - knight_count
        variants = ["knight"] * knight_count + ["archer"] * archer_count
        random.shuffle(variants)  # biar urutan spawn acak

        for variant in variants:
            platform = random.choice(platform_list)
            x_pos = random.randint(platform.rect.left, platform.rect.right)
            y_pos = platform.rect.top - 60

            goblin = Goblin(x_pos, y_pos, pygame.Surface((40, 60)), variant=variant)

            if variant == "knight":
                goblin.image.fill((255, 165, 0))  # oranye
            else:
                goblin.image.fill((0, 255, 255))  # cyan

            self.enemies.add(goblin)

    def _add_enemies(self):
        if self.level_number == 1:
            self.spawn_random_goblins(count=3)
        elif self.level_number == 2:
            self.spawn_random_goblins(count=4)
        elif self.level_number == 3:
            self.spawn_random_goblins(count=5)
        elif self.level_number == 4:
            self.spawn_random_goblins(count=6)
        elif self.level_number == 5:
            self.spawn_random_goblins(count=7)


    def build_level(self):
        if self.level_number == 1:
            self.build_level_1()
        elif self.level_number == 2:
            self.build_level_2()
        elif self.level_number == 3:
            self.build_level_3()
        elif self.level_number == 4:
            self.build_level_4()
        elif self.level_number == 5:
            self.build_level_5()
        elif self.level_number == 6:
            self.build_level_shaman()
        else:
            self.platforms.add(Platform(0, 550, 800, 50))
            self.platforms.add(Platform(200, 450, 150, 20))
            self.platforms.add(Platform(500, 400, 150, 20))
            self._add_items()
            self._add_enemies()

    def build_level_1(self):
        self.platforms.empty()
        self.items.empty()
        self.enemies.empty()  # Bersihkan grup musuh dulu

        weighted_blocks = [
            (block_flat_corridor, 1),
            (block_platform_high, 3),
            (block_gap_bridge, 2),
            (block_step_up, 2),
            (block_multi_path, 2)
        ]

        def weighted_choice(pairs, k):
            blocks = [pair[0] for pair in pairs]
            weights = [pair[1] for pair in pairs]
            return random.choices(blocks, weights=weights, k=k)

        def short_flat(x):
            return [Platform(x, 550, 500, 50, spawnable=False)], [], 500

        core_blocks = weighted_choice(weighted_blocks, k=5)
        x_offset = 0

        intro_platforms, intro_items, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        self.items.add(*intro_items)
        x_offset += intro_width

        for block_fn in core_blocks:
            platforms, items, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            self.items.add(*items)
            x_offset += width

        outro_platforms, outro_items, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        self.items.add(*outro_items)
        x_offset += outro_width

        portal_platforms, portal_items, portal_width = portal_block(x_offset)
        self.platforms.add(*portal_platforms)
        self.items.add(*portal_items)
        x_offset += portal_width

        self.platforms.add(*outro_platforms)
        self.items.add(*outro_items)
        x_offset += outro_width

        # --- Spawn musuh Goblin di posisi platform yang sesuai ---

        # Fungsi bantu cari platform berdasarkan x Goblin
        def find_platform_y(x_pos):
            for platform in self.platforms:
                if platform.rect.left <= x_pos <= platform.rect.right:
                    return platform.rect.top
            return 550  # fallback ke tanah jika tidak ketemu

        self._add_enemies()

        print("Level 1 dengan musuh Goblin sudah dibuat")

    def build_level_2(self):
        self.platforms.empty()
        self.items.empty()

        weighted_blocks = [
            (block_flat_corridor, 0.5),
            (block_platform_high, 3),
            (block_gap_bridge, 4),
            (block_step_up, 4),
            (block_multi_path, 4)
        ]

        def weighted_choice(pairs, k):
            blocks = [pair[0] for pair in pairs]
            weights = [pair[1] for pair in pairs]
            return random.choices(blocks, weights=weights, k=k)

        def short_flat(x):
            return [Platform(x, 550, 500, 50, spawnable=False)], [], 500

        core_blocks = weighted_choice(weighted_blocks, k=6)
        x_offset = 0

        intro_platforms, intro_items, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        self.items.add(*intro_items)
        x_offset += intro_width

        for block_fn in core_blocks:
            platforms, items, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            self.items.add(*items)
            x_offset += width

        outro_platforms, outro_items, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        self.items.add(*outro_items)
        x_offset += outro_width

        portal_platforms, portal_items, portal_width = portal_block(x_offset)
        self.platforms.add(*portal_platforms)
        self.items.add(*portal_items)
        x_offset += portal_width

        def find_platform_y(x_pos):
            for platform in self.platforms:
                if platform.rect.left <= x_pos <= platform.rect.right:
                    return platform.rect.top
            return 550  # fallback ke tanah jika tidak ketemu

        self._add_enemies()

        print("Level 2")

    def build_level_3(self):
        self.platforms.empty()
        self.items.empty()

        weighted_blocks = [
            (block_flat_corridor, 0.2),
            (block_platform_high, 5),
            (block_gap_bridge, 6),
            (block_step_up, 5),
            (block_multi_path, 5)
        ]

        def weighted_choice(pairs, k):
            blocks = [pair[0] for pair in pairs]
            weights = [pair[1] for pair in pairs]
            return random.choices(blocks, weights=weights, k=k)

        def short_flat(x):
            return [Platform(x, 550, 500, 50, spawnable=False)], [], 500

        core_blocks = weighted_choice(weighted_blocks, k=8)
        x_offset = 0

        intro_platforms, intro_items, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        self.items.add(*intro_items)
        x_offset += intro_width

        for block_fn in core_blocks:
            platforms, items, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            self.items.add(*items)
            x_offset += width

        outro_platforms, outro_items, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        self.items.add(*outro_items)
        x_offset += outro_width

        portal_platforms, portal_items, portal_width = portal_block(x_offset)
        self.platforms.add(*portal_platforms)
        self.items.add(*portal_items)
        x_offset += portal_width

        def find_platform_y(x_pos):
            for platform in self.platforms:
                if platform.rect.left <= x_pos <= platform.rect.right:
                    return platform.rect.top
            return 550  # fallback ke tanah jika tidak ketemu

        self._add_enemies()

        print("Level 3")

    def build_level_4(self):
        self.platforms.empty()
        self.items.empty()

        weighted_blocks = [
            (block_flat_corridor, 0.05),
            (block_platform_high, 6),
            (block_gap_bridge, 7),
            (block_step_up, 6),
            (block_multi_path, 6)
        ]

        def weighted_choice(pairs, k):
            blocks = [pair[0] for pair in pairs]
            weights = [pair[1] for pair in pairs]
            return random.choices(blocks, weights=weights, k=k)

        def short_flat(x):
            return [Platform(x, 550, 500, 50, spawnable=False)], [], 500

        core_blocks = weighted_choice(weighted_blocks, k=10)
        x_offset = 0

        intro_platforms, intro_items, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        self.items.add(*intro_items)
        x_offset += intro_width

        for block_fn in core_blocks:
            platforms, items, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            self.items.add(*items)
            x_offset += width

        outro_platforms, outro_items, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        self.items.add(*outro_items)
        x_offset += outro_width

        portal_platforms, portal_items, portal_width = portal_block(x_offset)
        self.platforms.add(*portal_platforms)
        self.items.add(*portal_items)
        x_offset += portal_width

        def find_platform_y(x_pos):
            for platform in self.platforms:
                if platform.rect.left <= x_pos <= platform.rect.right:
                    return platform.rect.top
            return 550  # fallback ke tanah jika tidak ketemu

        self._add_enemies()

        print("Level 4")

    def build_level_5(self):
        self.platforms.empty()
        self.items.empty()
        self.lava = pygame.sprite.Group()

        weighted_blocks = [
            (block_flat_corridor, 0.1),
            (block_platform_high, 4),
            (block_gap_bridge, 5),
            (block_step_up, 5),
            (block_multi_path, 4),
        ]

        def weighted_choice(pairs, k):
            blocks = [pair[0] for pair in pairs]
            weights = [pair[1] for pair in pairs]
            return random.choices(blocks, weights=weights, k=k)

        def short_flat(x):
            return [Platform(x, 550, 500, 50, spawnable=False)], [], 500

        core_blocks = weighted_choice(weighted_blocks, k=12)
        x_offset = 0

        # Intro
        intro_platforms, intro_items, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        self.items.add(*intro_items)
        x_offset += intro_width

        # Blok rintangan
        for block_fn in core_blocks:
            result = block_fn(x_offset)
            if len(result) == 3:
                platforms, items, width = result
            else:
                platforms, items, lava, width = result
                self.lava.add(*lava)
            self.platforms.add(*platforms)
            self.items.add(*items)
            x_offset += width

        # Outro platform
        outro_platforms, outro_items, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        self.items.add(*outro_items)
        x_offset += outro_width

        # Portal ke Level 6 (boss room)
        portal_platforms, portal_items, portal_width = portal_block(x_offset)
        self.platforms.add(*portal_platforms)
        self.items.add(*portal_items)
        x_offset += portal_width

        def find_platform_y(x_pos):
            for platform in self.platforms:
                if platform.rect.left <= x_pos <= platform.rect.right:
                    return platform.rect.top
            return 550  # fallback ke tanah jika tidak ketemu

        self._add_enemies()

        print("Level 5")

    def build_level_shaman(self):
        self.platforms.empty()
        self.items.empty()

        # === Desain Lorong Panjang (blok modular) ===
        corridor_width = 100
        corridor_height = 50
        corridor_length = 20
        corridor_x = 0
        corridor_y = 550

        # Membuat lorong panjang
        for i in range(corridor_length):
            platform = Platform(corridor_x, corridor_y + i * corridor_height, corridor_width, corridor_height)
            self.platforms.add(platform)

        # === Pintu Besar Menuju Ruang Boss ===
        door_width = 300
        door_height = 50
        door_x = corridor_x + corridor_length * corridor_width - door_width  # Posisi pintu di akhir lorong
        door_y = corridor_y + 20
        door = Platform(door_x, door_y, door_width, door_height)
        self.platforms.add(door)

        # === Ruang Boss ===
        boss_room_x = door_x + door_width
        boss_room_y = door_y - 200
        boss_room_width = 1200
        boss_room_height = 600

        # Lantai ruang boss
        floor = Platform(boss_room_x, boss_room_y + boss_room_height, boss_room_width, 50)
        self.platforms.add(floor)

        # Langit-langit ruang boss
        ceiling = Platform(boss_room_x, boss_room_y + boss_room_height - 100, boss_room_width, 30)
        self.platforms.add(ceiling)

        # Dinding kiri dan kanan ruang boss
        wall_left = Platform(boss_room_x, boss_room_y + boss_room_height - 150, 30, boss_room_height)
        self.platforms.add(wall_left)

        wall_right = Platform(boss_room_x + boss_room_width - 30, boss_room_y + boss_room_height - 150, 30, boss_room_height)
        self.platforms.add(wall_right)

        print("Shaman Boss Room")
        
    def _add_items(self):
        if self.level_number == 4:
            self.items.add(Item(250, 420, 'life'))
        elif self.level_number == 5:
            self.items.add(Item(700, 500, 'fireball'))
        elif self.level_number == 9:
            self.items.add(Item(600, 350, 'shield'))
        elif self.level_number == 14:
            self.items.add(Item(600, 350, 'life'))

class LevelManager:
    def __init__(self, player):  # Terima player sebagai parameter
        self.current_level = 1
        self.level = Level(self.current_level, player)  # Pass player ke Level

    def go_to_next_level(self):
        if self.current_level < 15:
            self.current_level += 1
            self.level = Level(self.current_level, self.level.player)  # Pass player ke Level

    def go_to_specific_level(self, level_number):
        self.current_level = level_number
        self.level = Level(level_number, self.level.player)

# === Modular Block Definitions ===

def block_flat_corridor(x):
    width = 700
    platforms = [Platform(x, 550, width, 50)]
    return platforms, [], width

def block_platform_high(x):
    width = 700
    platforms = [
        Platform(x, 500, 200, 30),
        Platform(x + 250, 400, 200, 30),
        Platform(x + 500, 300, 200, 30)
    ]
    items = [Item(x + 520, 270, 'life')]
    return platforms, items, width

def block_gap_bridge(x):
    left = 400
    gap = 120
    right = 400
    width = left + gap + right
    platforms = [
        Platform(x, 550, left, 50),
        Platform(x + left + gap, 550, right, 50)
    ]
    items = [Item(x + left + gap + 20, 500, 'shield')]
    return platforms, items, width

def block_step_up(x):
    width = 700
    platforms = [
        Platform(x, 550, 200, 50),
        Platform(x + 220, 500, 200, 50),
        Platform(x + 440, 450, 200, 50)
    ]
    return platforms, [], width

def block_multi_path(x):
    width = 700
    platforms = [
        Platform(x, 550, 300, 50),
        Platform(x + 350, 550, 300, 50),
        Platform(x + 150, 400, 150, 30),
        Platform(x + 400, 350, 150, 30)
    ]
    items = [Item(x + 420, 320, 'life')]
    return platforms, items, width

def portal_block(x):
    print(f"[DEBUG] Portal created at x={x+125}, y=500")
    platforms = [Platform(x, 550, 300, 50)]
    items = [Item(x + 125, 500, 'portal')]
    return platforms, items, 300

# Blok Lorong
def block_corridor(x, y, length):
    corridor_width = 100
    corridor_height = 50
    platforms = []
    for i in range(length):
        platform = SimplePlatform(x, y + i * corridor_height, corridor_width, corridor_height)
        platforms.append(platform)
    return platforms, [], length * corridor_width

# Blok Ruang Boss
def block_boss_room(x, y, room_width, room_height):
    platforms = []
    
    # Lantai ruang boss
    floor = SimplePlatform(x, y + room_height, room_width, 50)
    platforms.append(floor)

    # Langit-langit ruang boss
    ceiling = SimplePlatform(x, y + room_height - 100, room_width, 30)
    platforms.append(ceiling)

    # Dinding kiri dan kanan ruang boss
    wall_left = SimplePlatform(x, y + room_height - 150, 30, room_height)
    platforms.append(wall_left)

    wall_right = SimplePlatform(x + room_width - 30, y + room_height - 150, 30, room_height)
    platforms.append(wall_right)
    
    return platforms, [], room_width
