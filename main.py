import pygame
import sys
from level import LevelManager, Level
from player import Player
from assets import load_assets

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knightfall")
clock = pygame.time.Clock()
paused = False
assets = load_assets()
heart_image = assets["heart"]

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

def show_level_menu():
    font = pygame.font.SysFont(None, 50)
    level_buttons = []
    for i in range(1, 6):
        label = font.render(f"Level {i}", True, (255, 255, 255))
        rect = label.get_rect(center=(WIDTH // 2, 100 + i * 80))
        level_buttons.append((i, label, rect))

    waiting_for_release = True
    while waiting_for_release:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                waiting_for_release = False

    while True:
        screen.fill((30, 30, 30))
        for i, label, rect in level_buttons:
            screen.blit(label, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for level_num, _, rect in level_buttons:
                    if rect.collidepoint(event.pos):
                        return level_num

        pygame.display.flip()
        clock.tick(60)

def show_main_menu():
    font = pygame.font.SysFont(None, 60)
    while True:
        screen.fill((20, 20, 20))
        title = font.render("Knightfall", True, (255, 255, 255))
        play_text = font.render("Play", True, (0, 255, 0))
        exit_text = font.render("Exit", True, (255, 0, 0))

        title_rect = title.get_rect(center=(WIDTH // 2, 150))
        play_rect = play_text.get_rect(center=(WIDTH // 2, 300))
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, 400))

        screen.blit(title, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    selected_level = show_level_menu()
                    return selected_level
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

def show_pause_menu():
    font = pygame.font.SysFont(None, 60)
    while True:
        screen.fill((40, 40, 40))
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        continue_text = font.render("Lanjutkan", True, (0, 255, 0))
        exit_text = font.render("Keluar", True, (255, 0, 0))

        pause_rect = pause_text.get_rect(center=(WIDTH // 2, 150))
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, 300))
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, 400))

        screen.blit(pause_text, pause_rect)
        screen.blit(continue_text, continue_rect)
        screen.blit(exit_text, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(event.pos):
                    return "continue"
                elif exit_rect.collidepoint(event.pos):
                    return "exit"

        pygame.display.flip()
        clock.tick(60)

def game_over_menu():
    font = pygame.font.SysFont(None, 60)
    while True:
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        retry_text = font.render("Ulangi", True, (0, 255, 0))
        exit_text = font.render("Keluar", True, (255, 0, 0))

        go_rect = game_over_text.get_rect(center=(WIDTH // 2, 150))
        retry_rect = retry_text.get_rect(center=(WIDTH // 2, 300))
        exit_rect = exit_text.get_rect(center=(WIDTH // 2, 400))

        screen.blit(game_over_text, go_rect)
        screen.blit(retry_text, retry_rect)
        screen.blit(exit_text, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return "retry"
                elif exit_rect.collidepoint(event.pos):
                    return "exit"

        pygame.display.flip()
        clock.tick(60)

# === UI & Level Init ===
BG_COLOR = (30, 30, 30)
font = pygame.font.SysFont(None, 32)

def draw_text(text, x, y, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# MENU → LEVEL → GAMEPLAY
selected_level = show_main_menu()  # pilih level hanya sekali

# Buat level & player sesuai level yang dipilih
level = Level(selected_level, None)
player = Player(100, 400, level.enemies)
level.player = player

level_manager = LevelManager(player)
level_manager.current_level = selected_level
level_manager.level = level

camera_x = 0
MAX_LEVEL_WIDTH = 20000

def update_max_width():
    global MAX_LEVEL_WIDTH
    MAX_LEVEL_WIDTH = max((p.rect.right for p in level.platforms), default=800)

update_max_width()
last_spawn_x = 0

paused = False
game_over = False

running = True
while running:
    if not paused and not game_over:
        screen.fill((135, 206, 235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True

        keys = pygame.key.get_pressed()

        # Bekukan input saat cutscene
        if cutscene_active:
            keys = {k: False for k in range(512)}

        # Update player (gerakan, serangan, dll)
        player.update(level.platforms, keys)
        
        if player.is_game_over:
            game_over = True

        # Update musuh dan render
        for enemy in level.enemies:
            enemy.update(level.platforms, player)
            screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y))
            for proj in enemy.projectiles:
                screen.blit(proj.image, (proj.rect.x - camera_x, proj.rect.y))
                if proj.rect.colliderect(player.rect):
                    print("💥 Player terkena panah!")
                    player.take_damage()
                    proj.kill()

        # Kamera mengikuti player
        camera_x = player.rect.centerx - WIDTH // 2
        camera_x = max(0, min(camera_x, MAX_LEVEL_WIDTH - WIDTH))

        # Render platform, item, player, boss
        for platform in level.platforms:
            screen.blit(platform.image, (platform.rect.x - camera_x, platform.rect.y))
        for item in level.items:
            screen.blit(item.image, (item.rect.x - camera_x, item.rect.y))
            if item.type == 'portal' and player.rect.colliderect(item.rect):
                level_manager.go_to_next_level()
                level = level_manager.level
                update_max_width()
                player.rect.topleft = (100, 400)
                player.enemies = level.enemies  # update musuh di player

            # cek interaksi portal, teleport, boss trigger seperti biasa
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))
        for boss in boss_group:
            screen.blit(boss.image, (boss.rect.x - camera_x, boss.rect.y))

        # Tampilkan UI level
        draw_text(f"Level: {level.level_number}", 10, 10)

        # Cek pindah level dan update musuh di player
        if level_manager.current_level != level.level_number:
            level = level_manager.level
            player.enemies = level.enemies

        # Respawn dan kurangi nyawa jika jatuh
        if player.rect.y > HEIGHT + 200:
            player.take_damage()
            if player.lives <= 0:
                game_over = True
            else:
                print("😵 Player jatuh! Respawn...")
                player.rect.topleft = (100, 400)  # jangan buat ulang level

        # Gambar nyawa player
        for i in range(player.lives):
            x = 10 + i * (24 + 5)
            y = 50
            screen.blit(heart_image, (x, y))

    elif paused:
        choice = show_pause_menu()
        if choice == "continue":
            paused = False
        elif choice == "exit":
            selected_level = show_main_menu()
            level = Level(selected_level, None)
            player = Player(100, 400, level.enemies)
            level.player = player
            level_manager = LevelManager(player)
            level_manager.current_level = selected_level
            level_manager.level = level
            update_max_width()
            paused = False

    elif game_over:
        choice = game_over_menu()
        if choice == "retry":
            level = Level(level_manager.current_level, None)
            player = Player(100, 400, level.enemies)
            level.player = player
            level_manager.level = level
            update_max_width()
            game_over = False
        elif choice == "exit":
            selected_level = show_main_menu()
            level = Level(selected_level, None)
            player = Player(100, 400, level.enemies)
            level.player = player
            level_manager.current_level = selected_level
            level_manager.level = level
            update_max_width()
            game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
