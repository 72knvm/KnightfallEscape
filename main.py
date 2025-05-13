import pygame
import sys
from level import LevelManager, Level
from player import Player

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knightfall")
clock = pygame.time.Clock()

# === Boss & Cutscene System ===
boss_group = pygame.sprite.Group()
boss_spawned = False
cutscene_active = False

cutscene_lines = [
    "Saman: Hmm...? Seorang manusia...?",
    "Saman: Sudah bertahun-tahun sejak jejak terakhir menginjak tanah ini.",
    "Saman: Apa yang membawamu ke kegelapan seperti ini?",
    "Ksatria: Aku terjatuh... dan saat terbangun, aku sudah di tempat ini.",
    "Ksatria: Kau... apakah kau penjaga dunia ini?",
    "Saman: Penjaga? Hah...",
    "Saman: Akulah penguasa dasar dunia ini. Raja dari kehampaan.",
    "Ksatria: Aku hanya ingin keluar. Biarkan aku pergi!",
    "Saman: Hahaha... keluar?",
    "Saman: Tidak, manusia. Tak ada yang keluar dari sini.",
    "Saman: Sudah lama aku tak mencicipi darah manusia...",
    "Saman: Malam ini... sepertinya aku akan berpesta."
]

current_line = 0
line_timer = 0

# === UI & Level Init ===
BG_COLOR = (30, 30, 30)
font = pygame.font.SysFont(None, 32)

def draw_text(text, x, y, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

level_manager = LevelManager()
level = level_manager.level
player = Player(100, 400)
player_group = pygame.sprite.Group(player)

camera_x = 0
velocity_y = 0
MAX_LEVEL_WIDTH = 20000

def update_max_width():
    global MAX_LEVEL_WIDTH
    MAX_LEVEL_WIDTH = max((p.rect.right for p in level.platforms), default=800)

update_max_width()
running = True

while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Bekukan input saat cutscene
    if cutscene_active:
        keys = {k: False for k in range(512)}

    player.update(level.platforms, keys)

    camera_x = player.rect.centerx - WIDTH // 2
    camera_x = max(0, min(camera_x, MAX_LEVEL_WIDTH - WIDTH))

    # Gambar platform
    for platform in level.platforms:
        screen.blit(platform.image, (platform.rect.x - camera_x, platform.rect.y))

    # Gambar item + logic
    for item in level.items:
        screen.blit(item.image, (item.rect.x - camera_x, item.rect.y))
        if item.type == 'portal' and player.rect.colliderect(item.rect):
            level_manager.go_to_next_level()
            level = level_manager.level
            update_max_width()
            player.rect.topleft = (100, 400)
            velocity_y = 0
        elif item.type == 'teleport' and player.rect.colliderect(item.rect):
            print("🌀 Teleporting to boss room...")
            player.rect.x = MAX_LEVEL_WIDTH - 900
            player.rect.y = 400
        elif item.type == 'boss_trigger' and player.rect.colliderect(item.rect) and not cutscene_active:
            print("🎬 Cutscene dimulai...")
            cutscene_active = True
            current_line = 0
            line_timer = pygame.time.get_ticks()

    # Gambar player
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

    # Gambar boss
    for boss in boss_group:
        screen.blit(boss.image, (boss.rect.x - camera_x, boss.rect.y))

    # Dialog saat cutscene
    if cutscene_active:
        if pygame.time.get_ticks() - line_timer > 3000:
            current_line += 1
            line_timer = pygame.time.get_ticks()

            if current_line >= len(cutscene_lines):
                cutscene_active = False
                boss_spawned = True

                # Spawn boss di posisi singgasana
                for item in level.items:
                    if item.type == 'boss_throne':
                        from boss import BossSaman
                        boss = BossSaman(item.rect.x, item.rect.y - 60)
                        boss_group.add(boss)
                        break
        else:
            draw_text(cutscene_lines[current_line], WIDTH // 2 - 200, HEIGHT // 2 - 40)

    # UI teks
    draw_text(f"Level: {level.level_number}", 10, 10)
    draw_text(f"State: {level.state}", 10, 40)

    # Respawn jika jatuh
    if player.rect.y > HEIGHT + 200:
        print("😵 Player fell!")
        level = Level(level_manager.current_level)
        update_max_width()
        player.rect.topleft = (100, 400)
        velocity_y = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
