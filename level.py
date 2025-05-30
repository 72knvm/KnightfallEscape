import pygame
from game_platform import Platform, Item
import random
from goblin import Goblin
from player import find_spawn_y
from game_platform import AnimatedPortal

class SimplePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((169, 169, 169))  # Warna abu-abu untuk platform
        self.rect = self.image.get_rect(topleft=(x, y))

MAX_LEVEL_WIDTH = 20000  # pastikan ini nilai level kamu sesuai

class Level:
    def __init__(self, level_number, player, assets):
        self.level_number = level_number
        self.player = player  # Simpan objek player yang diterima
        self.assets = assets
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boss = None
        self.portal = None  # untuk menyimpan item portal

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
        random.shuffle(variants)

        for variant in variants:
            platform = random.choice(platform_list)
            x_pos = random.randint(platform.rect.left, platform.rect.right)
            y_pos = platform.rect.top - 60

            # ✅ Kirim semua assets, Goblin akan memilih sesuai variant
            goblin = Goblin(x_pos, y_pos, image=None, variant=variant, assets=self.assets)

            self.enemies.add(goblin)

    def spawn_random_potions(self, count=3):
        self.items = pygame.sprite.Group()
        image_dict = {
            "health": self.assets.get("health_potion"),
            "shield": self.assets.get("shield_potion")
        }

        spawnable_platforms = [p for p in self.platforms if getattr(p, "spawnable", True)]

        if not spawnable_platforms:
            print("[WARNING] Tidak ada platform valid untuk spawn potion.")
            return

        from random import choice, randint

        for _ in range(count):
            platform = choice(spawnable_platforms)
            item_type = choice(["health", "shield"])
            item_img = image_dict[item_type]
            item_height = item_img.get_height() if item_img else 30

            x_pos = randint(platform.rect.left, platform.rect.right - 30)
            y_pos = platform.rect.top - item_height

            item = Item(x_pos, y_pos, item_type, image_dict)
            self.items.add(item)

    def _add_items(self):
        self.items = pygame.sprite.Group()
        image_dict = {
            "health": self.assets.get("health_potion"),
            "shield": self.assets.get("shield_potion")
        }
        item_height = image_dict["health"].get_height()
        y = 550 - item_height

        self.items.add(Item(300, y, "health", image_dict))
        self.items.add(Item(600, y, "shield", image_dict))

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
        self.enemies.empty()
        self.portal = None  # untuk menyimpan portal animasi

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
            platforms = [Platform(x, 550, 500, 50, spawnable=False, image=self.assets["platform"])]
            return platforms, 500

        core_blocks = weighted_choice(weighted_blocks, k=5)
        x_offset = 0

        # Platform awal
        intro_platforms, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        x_offset += intro_width

        # Tambahkan blok random utama
        for block_fn in core_blocks:
            platforms, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            x_offset += width

        # Platform akhir sebelum portal
        outro_platforms, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        x_offset += outro_width

        # Tambahkan portal
        portal_platforms, portal_items, portal_width = portal_block(x_offset, self.assets)
        self.platforms.add(*portal_platforms)
        self.portal = portal_items[0]  # simpan objek portal
        x_offset += portal_width

        # Tambahkan item (potion)
        self.spawn_random_potions(count=3)

        self._add_enemies()
        print("Level 1 dengan musuh Goblin sudah dibuat")

    def build_level_2(self):
        self.platforms.empty()
        self.enemies.empty()
        self.portal = None  # untuk menyimpan portal animasi

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
            platforms = [Platform(x, 550, 500, 50, spawnable=False, image=self.assets["platform"])]
            return platforms, 500

        core_blocks = weighted_choice(weighted_blocks, k=6)
        x_offset = 0

        # Platform awal
        intro_platforms, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        x_offset += intro_width

        # Tambahkan blok utama random
        for block_fn in core_blocks:
            platforms, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            x_offset += width

        # Platform penutup sebelum portal
        outro_platforms, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        x_offset += outro_width

        # Tambahkan portal
        portal_platforms, portal_items, portal_width = portal_block(x_offset, self.assets)
        self.platforms.add(*portal_platforms)
        self.portal = portal_items[0]
        x_offset += portal_width

        # ✅ Urutan yang tepat: Tambahkan potion dulu, lalu musuh
        self.spawn_random_potions(count=4)
        self._add_enemies()

        print("Level 2 dengan portal dan potion sudah dibuat")

    def build_level_3(self):
        self.platforms.empty()
        self.enemies.empty()
        self.portal = None  # untuk menyimpan portal animasi

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
            platforms = [Platform(x, 550, 500, 50, spawnable=False, image=self.assets["platform"])]
            return platforms, 500

        core_blocks = weighted_choice(weighted_blocks, k=8)
        x_offset = 0

        # Platform awal
        intro_platforms, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        x_offset += intro_width

        # Tambahkan blok utama random
        for block_fn in core_blocks:
            platforms, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            x_offset += width

        # Platform penutup sebelum portal
        outro_platforms, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        x_offset += outro_width

        # Tambahkan portal
        portal_platforms, portal_items, portal_width = portal_block(x_offset, self.assets)
        self.platforms.add(*portal_platforms)
        self.portal = portal_items[0]
        x_offset += portal_width

        # ✅ Tambahkan potion terlebih dahulu
        self.spawn_random_potions(count=5)

        # ✅ Lalu musuh
        self._add_enemies()

        print("Level 3 dengan portal dan potion sudah dibuat")

    def build_level_4(self):
        self.platforms.empty()
        self.enemies.empty()
        self.portal = None  # menyimpan portal animasi

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
            platforms = [Platform(x, 550, 500, 50, spawnable=False, image=self.assets["platform"])]
            return platforms, 500

        core_blocks = weighted_choice(weighted_blocks, k=10)
        x_offset = 0

        # Platform awal
        intro_platforms, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        x_offset += intro_width

        # Blok utama
        for block_fn in core_blocks:
            platforms, width = block_fn(x_offset)
            self.platforms.add(*platforms)
            x_offset += width

        # Outro platform sebelum portal
        outro_platforms, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        x_offset += outro_width

        # Tambahkan portal
        portal_platforms, portal_items, portal_width = portal_block(x_offset, self.assets)
        self.platforms.add(*portal_platforms)
        self.portal = portal_items[0]
        x_offset += portal_width

        # ✅ Potion dulu
        self.spawn_random_potions(count=6)

        # ✅ Baru musuh
        self._add_enemies()

        print("Level 4 dengan portal dan potion sudah dibuat")

    def build_level_5(self):
        self.platforms.empty()
        self.enemies.empty()
        self.lava = pygame.sprite.Group()
        self.portal = None  # simpan portal animasi

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
            platforms = [Platform(x, 550, 500, 50, spawnable=False, image=self.assets["platform"])]
            return platforms, 500

        core_blocks = weighted_choice(weighted_blocks, k=12)
        x_offset = 0

        # Platform awal
        intro_platforms, intro_width = short_flat(x_offset)
        self.platforms.add(*intro_platforms)
        x_offset += intro_width

        # Blok rintangan
        for block_fn in core_blocks:
            result = block_fn(x_offset)
            if len(result) == 2:
                platforms, width = result
            elif len(result) == 3:
                platforms, width, lava = result
                self.lava.add(*lava)
            else:
                platforms, _, lava, width = result
                self.lava.add(*lava)
            self.platforms.add(*platforms)
            x_offset += width

        # Outro platform
        outro_platforms, outro_width = short_flat(x_offset)
        self.platforms.add(*outro_platforms)
        x_offset += outro_width

        # Portal menuju Level 6
        portal_platforms, portal_items, portal_width = portal_block(x_offset, self.assets)
        self.platforms.add(*portal_platforms)
        self.portal = portal_items[0]
        x_offset += portal_width

        # ✅ Potion dulu agar player bisa interaksi
        self.spawn_random_potions(count=7)

        # ✅ Lalu musuh
        self._add_enemies()

        print("Level 5 dengan portal dan potion sudah dibuat")

    def build_level_shaman(self):
        self.platforms.empty()

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
        
class LevelManager:
    def __init__(self, player, assets):
        self.current_level = 1
        self.level = Level(self.current_level, player, assets)
        self.assets = assets

    def go_to_next_level(self):
        self.current_level += 1
        # Buat level baru dengan player yang sama
        self.level = Level(self.current_level, self.level.player, self.assets)

        # Tentukan spawn_x sesuai level, bisa juga disimpan per level
        spawn_x = 100
        player_height = self.level.player.rect.height
        spawn_y = find_spawn_y(self.level.platforms, spawn_x, player_height)

        # Reset posisi player di level baru
        self.level.player.reset(x=spawn_x, y=spawn_y, platforms=self.level.platforms)

        self.level.player.items = self.level.items 

    def go_to_specific_level(self, level_number):
        self.current_level = level_number
        self.level = Level(level_number, self.level.player, self.assets)

        # Sama seperti go_to_next_level, reset posisi player di level spesifik
        spawn_x = 100
        player_height = self.level.player.rect.height
        spawn_y = find_spawn_y(self.level.platforms, spawn_x, player_height)
        self.level.player.reset(x=spawn_x, y=spawn_y, platforms=self.level.platforms)

# === Modular Block Definitions ===

def block_flat_corridor(x):
    width = 700
    platforms = [Platform(x, 550, width, 50)]
    return platforms, width

def block_platform_high(x):
    width = 700
    platforms = [
        Platform(x, 500, 200, 30),
        Platform(x + 250, 400, 200, 30),
        Platform(x + 500, 300, 200, 30)
    ]
    return platforms, width

def block_gap_bridge(x):
    left = 400
    gap = 120
    right = 400
    width = left + gap + right
    platforms = [
        Platform(x, 550, left, 50),
        Platform(x + left + gap, 550, right, 50)
    ]
    return platforms, width

def block_step_up(x):
    width = 700
    gap = 50
    platforms = [
        Platform(x, 550, 200, 50),
        Platform(x + 220 + gap, 500, 200, 100),     # tambah gap di sini
        Platform(x + 440 + 2 * gap, 450, 200, 150)  # tambah gap di sini
    ]
    return platforms, width

def block_multi_path(x):
    width = 700
    platforms = [
        Platform(x, 550, 300, 50),
        Platform(x + 350, 550, 300, 50),
        Platform(x + 150, 450, 150, 30),
        Platform(x + 400, 400, 150, 30)
    ]
    return platforms, width

def portal_block(x, assets):
    platform_y = 550
    platform_height = 50
    portal_height = assets["portal"][0].get_height()

    # Posisi visual sprite (tapi rect tetap di logika yang akurat)
    portal_y = platform_y - portal_height  # logika dasar untuk rect
    render_offset_y = 25  # sesuaikan agar sprite sejajar atas platform
    render_offset_x = 120  # geser horizontal agar sprite pas di tengah

    platforms = [Platform(x, platform_y, 300, platform_height)]
    portal = AnimatedPortal(x + 86, portal_y, assets["portal"],
                            render_offset_x=render_offset_x,
                            render_offset_y=render_offset_y)
    
    return platforms, [portal], 300
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
