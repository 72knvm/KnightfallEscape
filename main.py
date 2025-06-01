import pygame
import sys
import os
from level import LevelManager, Level
from player import Player
from assets import load_assets
from boss_saman import BossSaman

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knightfall")
clock = pygame.time.Clock()
paused = False

assets = load_assets()

# Global fonts
base_path = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(base_path, "fonts", "Cinzel-Regular.ttf")
if not os.path.exists(FONT_PATH):
    print("[ERROR] Font path tidak ditemukan:", FONT_PATH)
cinzel_font_large = pygame.font.Font(FONT_PATH, 60)
cinzel_font_medium = pygame.font.Font(FONT_PATH, 36)
cinzel_font_small = pygame.font.Font(FONT_PATH, 24)

bg_image = assets["main_menu_bg"]
level_bg = pygame.transform.scale(assets["level_bg"], (WIDTH, HEIGHT))
idle_frames = assets['idle']

# Tambahkan ini supaya animasi berjalan siap pakai
walk_right_frames = assets['walk_right']
walk_left_frames = assets['walk_left']

# === Boss & Cutscene System ===
boss_group = pygame.sprite.Group()
boss_spawned = False
cutscene_active = False

boss_defeated = False

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

def draw_text_with_shadow(surface, text, font, text_color, pos, shadow_color=(0, 0, 0), offset=2):
    shadow = font.render(text, True, shadow_color)
    text_surf = font.render(text, True, text_color)
    x, y = pos
    surface.blit(shadow, (x + offset, y + offset))
    surface.blit(text_surf, (x, y))
    
def find_spawn_y(platforms, spawn_x, player_height):
    candidates = [p for p in platforms if p.rect.left <= spawn_x <= p.rect.right]
    if not candidates:
        print(f"[WARN] Tidak ada platform untuk x={spawn_x}, fallback y=400")
        return 400
    highest_platform = min(candidates, key=lambda p: p.rect.top)
    spawn_y = highest_platform.rect.top - player_height
    print(f"Spawn Y untuk x={spawn_x} adalah {spawn_y} dari platform {highest_platform.rect}")
    return spawn_y

def show_level_menu():
    font = cinzel_font_medium
    level_buttons = []
    base_y = 100
    spacing = 60

    level_labels = {
        1: "Level 1",
        2: "Level 2",
        3: "Level 3",
        4: "Level 4",
        5: "Level 5",
        6: "Boss: Shaman"  # ⬅️ Ini label khusus
    }

    for i in range(1,7):
        rect = font.render(f"Level {i}", True, (255, 255, 255)).get_rect(center=(WIDTH // 2, base_y + i * spacing))
        level_buttons.append((i, rect))

    back_rect = font.render("Back", True, (255, 255, 0)).get_rect(center=(WIDTH // 2, HEIGHT - 60))

    waiting_for_release = True
    while waiting_for_release:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                waiting_for_release = False

    while True:
        screen.blit(pygame.transform.scale(assets["level_bg"], (WIDTH, HEIGHT)), (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for level_num, rect in level_buttons:
            color = (255, 255, 255)
            if rect.collidepoint(mouse_pos):
                color = (144, 238, 144)  # light green hover
                if mouse_click[0]:
                    return level_num
            draw_text_with_shadow(screen, f"Level {level_num}", font, color, rect.topleft)

        back_color = (255, 255, 0)
        if back_rect.collidepoint(mouse_pos):
            back_color = (255, 255, 150)
            if mouse_click[0]:
                return "back"
        draw_text_with_shadow(screen, "Back", font, back_color, back_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def show_main_menu():
    global WIDTH, HEIGHT, screen
    cinzel_font = cinzel_font_large
    button_font = cinzel_font_medium
    credit_font = pygame.font.SysFont(None, 24)
    play_music("Backsound/Main Song.mp3")
    bg_image = assets["main_menu_bg"]

    while True:
        screen.fill((20, 20, 20))
        scaled_bg = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))

        title_text = "Knightfall"
        title_rect = cinzel_font.render(title_text, True, (44, 44, 44)).get_rect(center=(WIDTH // 2, 150))

        # Hover effect colors
        play_color = (46, 204, 113)
        options_color = (241, 196, 15)
        exit_color = (231, 76, 60)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        play_rect = button_font.render("Play", True, play_color).get_rect(center=(WIDTH // 2, 300))
        options_rect = button_font.render("Options", True, options_color).get_rect(center=(WIDTH // 2, 370))
        exit_rect = button_font.render("Exit", True, exit_color).get_rect(center=(WIDTH // 2, 440))

        if play_rect.collidepoint(mouse_pos):
            play_color = (88, 214, 141)
            if mouse_click[0]:
                selected_level = show_level_menu()
                if selected_level == "back":
                    continue
                elif isinstance(selected_level, int):
                    return selected_level

        if options_rect.collidepoint(mouse_pos):
            options_color = (253, 203, 110)
            if mouse_click[0]:
                choice = show_options_menu()
                if choice == "back":
                    continue
                elif choice == "menu":
                    return "menu"
                elif isinstance(choice, tuple):
                    WIDTH, HEIGHT = choice
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

        if exit_rect.collidepoint(mouse_pos):
            exit_color = (255, 99, 71)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()

        draw_text_with_shadow(screen, title_text, cinzel_font, (44, 44, 44), title_rect.topleft)
        draw_text_with_shadow(screen, "Play", button_font, play_color, play_rect.topleft)
        draw_text_with_shadow(screen, "Options", button_font, options_color, options_rect.topleft)
        draw_text_with_shadow(screen, "Exit", button_font, exit_color, exit_rect.topleft)

        credit_text = credit_font.render("Music : FROST by Alexander Nakarada", True, (200, 200, 200))
        screen.blit(credit_text, (10, HEIGHT - 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def show_pause_menu():
    font = cinzel_font_medium
    while True:
        screen.blit(pygame.transform.scale(assets["level_bg"], (WIDTH, HEIGHT)), (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Default Colors
        continue_color = (0, 255, 0)
        option_color = (255, 255, 0)
        menu_color = (255, 0, 0)

        # Render rectangles
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, 150))

        continue_rect = font.render("Lanjutkan", True, continue_color).get_rect(center=(WIDTH // 2, 300))
        option_rect = font.render("Option", True, option_color).get_rect(center=(WIDTH // 2, 360))
        menu_rect = font.render("Main Menu", True, menu_color).get_rect(center=(WIDTH // 2, 420))

        # Hover effects and actions
        if continue_rect.collidepoint(mouse_pos):
            continue_color = (100, 255, 100)
            if mouse_click[0]:
                return "continue"

        if option_rect.collidepoint(mouse_pos):
            option_color = (255, 255, 150)
            if mouse_click[0]:
                choice = show_options_menu()
                if choice == "back":
                    continue
                elif choice == "menu":
                    return "menu"


        if menu_rect.collidepoint(mouse_pos):
            menu_color = (255, 100, 100)
            if mouse_click[0]:
                return "menu"

        # Draw all elements
        draw_text_with_shadow(screen, "PAUSED", font, (255, 255, 255), pause_rect.topleft)
        draw_text_with_shadow(screen, "Lanjutkan", font, continue_color, continue_rect.topleft)
        draw_text_with_shadow(screen, "Option", font, option_color, option_rect.topleft)
        draw_text_with_shadow(screen, "Main Menu", font, menu_color, menu_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def game_over_menu():
    font = cinzel_font_medium
    while True:
        screen.blit(pygame.transform.scale(assets["level_bg"], (WIDTH, HEIGHT)), (0, 0))
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

def show_victory_menu():
    font = cinzel_font_medium
    play_music("Backsound/victory.mp3", loop=False)
    while True:
        screen.blit(pygame.transform.scale(assets["victory_bg"], (WIDTH, HEIGHT)), (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # === Victory Title ===
        victory_text = "VICTORY!"
        victory_rect = font.render(victory_text, True, (255, 255, 0)).get_rect(center=(WIDTH // 2, 200))
        draw_text_with_shadow(screen, victory_text, font, (255, 255, 0), victory_rect.topleft)

        # === Main Menu Button ===
        menu_color = (0, 255, 0)
        hover_color = (100, 255, 100)

        menu_rect = font.render("Main Menu", True, menu_color).get_rect(center=(WIDTH // 2, 350))
        if menu_rect.collidepoint(mouse_pos):
            draw_text_with_shadow(screen, "Main Menu", font, hover_color, menu_rect.topleft)
            if mouse_click[0]:
                return "victory_main_menu"
        else:
            draw_text_with_shadow(screen, "Main Menu", font, menu_color, menu_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)
        
def show_resolution_selector():
    font = cinzel_font_medium
    resolutions = [
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1366, 768),
        (1920, 1080),
    ]

    index = 0  # index resolusi saat ini

    while True:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        # Default warna
        left_color = (255, 255, 255)
        right_color = (255, 255, 255)
        change_color = (0, 255, 0)
        back_color = (255, 255, 0)

        # Hover efek
        left_rect = font.render("<", True, left_color).get_rect(center=(WIDTH // 2 - 150, HEIGHT // 2))
        right_rect = font.render(">", True, right_color).get_rect(center=(WIDTH // 2 + 150, HEIGHT // 2))
        change_rect = font.render("Change", True, change_color).get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        back_rect = font.render("Back", True, back_color).get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170))

        if left_rect.collidepoint(mouse_pos):
            left_color = (200, 200, 255)
        if right_rect.collidepoint(mouse_pos):
            right_color = (200, 200, 255)
        if change_rect.collidepoint(mouse_pos):
            change_color = (100, 255, 100)
        if back_rect.collidepoint(mouse_pos):
            back_color = (255, 255, 150)

        # Tampilkan elemen
        title = font.render("Pilih Resolusi", True, (0, 255, 0))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150)))

        screen.blit(font.render("<", True, left_color), left_rect)
        screen.blit(font.render(">", True, right_color), right_rect)

        res_text = font.render(f"{resolutions[index][0]} x {resolutions[index][1]}", True, (255, 255, 255))
        screen.blit(res_text, res_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        screen.blit(font.render("Change", True, change_color), change_rect)
        screen.blit(font.render("Back", True, back_color), back_rect)

        # EVENT HANDLING (klik satu kali)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_rect.collidepoint(event.pos):
                    index = (index - 1) % len(resolutions)
                elif right_rect.collidepoint(event.pos):
                    index = (index + 1) % len(resolutions)
                elif change_rect.collidepoint(event.pos):
                    return resolutions[index]
                elif back_rect.collidepoint(event.pos):
                    return "back"

        pygame.display.flip()
        clock.tick(60)

def show_options_menu():
    global volume, is_muted, WIDTH, HEIGHT, screen
    font = cinzel_font_medium

    while True:
        screen.blit(pygame.transform.scale(assets["level_bg"], (WIDTH, HEIGHT)), (0, 0))

        x_center = WIDTH // 2
        start_y = int(HEIGHT * 0.2)
        line_height = int(HEIGHT * 0.11)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # TITLE
        draw_text_with_shadow(screen, "Settings", font, (255, 255, 255), (x_center - 90, int(HEIGHT * 0.08)))

        # === DISPLAY OPTIONS ===
        res_color = (200, 200, 200)
        fs_color = (241, 196, 15)

        resolution_rect = font.render("Change Resolution", True, res_color).get_rect(center=(x_center, start_y))
        fullscreen_rect = font.render("Fullscreen", True, fs_color).get_rect(center=(x_center, start_y + line_height))

        if resolution_rect.collidepoint(mouse_pos):
            res_color = (255, 255, 255)
        if fullscreen_rect.collidepoint(mouse_pos):
            fs_color = (253, 203, 110)

        draw_text_with_shadow(screen, "Change Resolution", font, res_color, resolution_rect.topleft)
        draw_text_with_shadow(screen, "Fullscreen", font, fs_color, fullscreen_rect.topleft)

        # === AUDIO OPTIONS ===
        vol_text = f"Volume: {int(volume * 100)}%"
        draw_text_with_shadow(screen, vol_text, font, (255, 255, 255), (x_center - 130, start_y + 2 * line_height))

        vol_up_color = (255, 255, 255)
        vol_down_color = (255, 255, 255)

        vol_up_rect = font.render("Volume +", True, vol_up_color).get_rect(center=(x_center, start_y + 3 * line_height))
        vol_down_rect = font.render("Volume -", True, vol_down_color).get_rect(center=(x_center, start_y + 4 * line_height))

        if vol_up_rect.collidepoint(mouse_pos):
            vol_up_color = (255, 255, 100)
        if vol_down_rect.collidepoint(mouse_pos):
            vol_down_color = (255, 255, 100)

        draw_text_with_shadow(screen, "Volume +", font, vol_up_color, vol_up_rect.topleft)
        draw_text_with_shadow(screen, "Volume -", font, vol_down_color, vol_down_rect.topleft)

        # === MUTE ===
        mute_color = (231, 76, 60) if is_muted or volume == 0 else (46, 204, 113)
        mute_text_surf = font.render("Mute", True, mute_color)
        mute_x = x_center - mute_text_surf.get_width() // 2
        mute_y = start_y + 5 * line_height
        mute_rect = pygame.Rect(mute_x, mute_y, mute_text_surf.get_width(), font.get_height())

        if mute_rect.collidepoint(mouse_pos):
            mute_color = (255, 99, 71) if is_muted or volume == 0 else (88, 214, 141)
            mute_text_surf = font.render("Mute", True, mute_color)

        screen.blit(mute_text_surf, (mute_x, mute_y))

        # === BACK ===
        back_color = (255, 215, 25)
        back_rect = font.render("Back", True, back_color).get_rect(center=(x_center, int(HEIGHT * 0.9)))

        if back_rect.collidepoint(mouse_pos):
            back_color = (255, 255, 100)

        draw_text_with_shadow(screen, "Back", font, back_color, back_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return "back"
                if resolution_rect.collidepoint(event.pos):
                    choice = show_resolution_selector()
                    if choice != "back":
                        WIDTH, HEIGHT = choice
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                if fullscreen_rect.collidepoint(event.pos):
                    toggle_fullscreen()
                if vol_up_rect.collidepoint(event.pos):
                    set_volume(volume + 0.1)
                if vol_down_rect.collidepoint(event.pos):
                    set_volume(volume - 0.1)
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()

        pygame.display.flip()
        clock.tick(60)

is_fullscreen = False

def toggle_fullscreen():
    global is_fullscreen, screen, WIDTH, HEIGHT

    if not is_fullscreen:
        info = pygame.display.Info()
        WIDTH, HEIGHT = info.current_w, info.current_h
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        is_fullscreen = True
    else:
        WIDTH, HEIGHT = 800, 600  # atau resolusi default
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        is_fullscreen = False

import pygame

def play_music(relative_path, loop=True):
    try:
        base_path = os.path.dirname(__file__)
        music_path = os.path.join(base_path, relative_path)

        if not os.path.exists(music_path):
            print(f"⚠️ Musik tidak ditemukan: {music_path}")
            return

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1 if loop else 0)
        print(f"🎵 Memutar musik: {relative_path}")
    except pygame.error as e:
        print(f"❌ Error memuat musik '{relative_path}': {e}")

def stop_music():
    pygame.mixer.music.stop()

volume = 1.0  # volume default penuh
is_muted = False

def set_volume(vol):
    global volume, is_muted
    volume = max(0.0, min(1.0, vol))  # batasi 0-1
    if volume == 0:
        mute_text = "🔇 Unmute"
    else:
        mute_text = "🔊 Mute"
    pygame.mixer.music.set_volume(volume)

def toggle_mute():
    global is_muted, volume
    if is_muted:
        pygame.mixer.music.set_volume(volume)
        is_muted = False
    else:
        pygame.mixer.music.set_volume(0.0)
        is_muted = True
        
# === UI & Level Init ===
BG_COLOR = (30, 30, 30)
font = pygame.font.SysFont(None, 32)

def draw_text(text, x, y, font=None, color=(255, 255, 255)):
    if font is None:
        font = cinzel_font_small
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# MENU → LEVEL → GAMEPLAY
while True:
    selected_level = show_main_menu()
    if isinstance(selected_level, int):
        break

# untuk stop music di gameplay
stop_music()

# Buat level sesuai pilihan
level = Level(selected_level, None, assets)

# Tentukan posisi spawn horizontal dan tinggi player
spawn_x = 100
player_height = 70  # sesuaikan dengan sprite playerd

# Hitung posisi spawn Y dari platform level
spawn_y = find_spawn_y(level.platforms, spawn_x, player_height)

# Buat objek player di posisi spawn tepat dengan semua animasi
player = Player(
    spawn_x,
    spawn_y,
    level.enemies,
    assets['idle'],        # idle frames (list)
    assets['walk_right'],  # walk right frames (list)
    assets['walk_left'],   # walk left frames (list)
    assets['jump'],        # jump frames (list)
    assets['attack'],       # attack frames (list)
    assets['hurt'],         # hit frames
    platforms=level.platforms,
    assets=assets
)
player.parry_frames = assets['parry']
player.death_frames = assets["death"]

level.player = player
player.items = level.items

level_manager = LevelManager(player, assets)
level_manager.current_level = selected_level
level_manager.level = level

play_music("Backsound/Level Song.mp3")

camera_x = 0
MAX_LEVEL_WIDTH = 20000
MAX_LEVEL_HEIGHT = 600  # tinggi level sesuai desain level

def update_max_width():
    global MAX_LEVEL_WIDTH
    MAX_LEVEL_WIDTH = max((p.rect.right for p in level.platforms), default=800)

update_max_width()
last_spawn_x = 0

paused = False
game_over = False

VIEWPORT_WIDTH = 800
VIEWPORT_HEIGHT = 450  # sesuaikan aspect ratio layar kamu

bg_x = 0

# Buat surface viewport tetap
viewport_surface = pygame.Surface((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))

running = True
while running:
    if not paused and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True

        keys = pygame.key.get_pressed()
        if cutscene_active:
            keys = {k: False for k in range(512)}

        dt = clock.tick(60) / 1000  # waktu frame dalam detik
        keys = pygame.key.get_pressed()
        player.update(level.platforms, keys, dt)

        if level.level_number == 6 and not level.boss_spawned:
            if player.rect.x > level.arena_x + 100:  # offset 50 px dari gerbang masuk
                level.trigger_boss()

        if player.is_game_over and not player.playing_death:
            game_over = True
                    
        # Hitung posisi kamera dengan viewport konstan
        camera_x = player.rect.centerx - VIEWPORT_WIDTH // 2
        camera_y = player.rect.centery - VIEWPORT_HEIGHT // 2
        camera_x = max(0, min(camera_x, MAX_LEVEL_WIDTH - VIEWPORT_WIDTH))
        camera_y = max(0, min(camera_y, MAX_LEVEL_HEIGHT - VIEWPORT_HEIGHT))

        # Bersihkan viewport surface
        viewport_surface.fill((135, 206, 235))  # warna langit

        # Pastikan bg_x sudah dideklarasikan sebelum loop (misal bg_x = 0)

        bg_width = level_bg.get_width()

        # Update posisi bg_x sesuai kamera (camera_x) setiap frame
        bg_x = -camera_x % bg_width  # modulus supaya looping mulus

        # Render background dua kali supaya tidak ada celah saat scrolling
        viewport_surface.blit(level_bg, (bg_x - bg_width, 0))
        viewport_surface.blit(level_bg, (bg_x, 0))

        # Render platform ke viewport surface
        for platform in level.platforms:
            viewport_surface.blit(platform.image, (platform.rect.x - camera_x, platform.rect.y - camera_y))
                
        for item in level.items:
            screen_x = item.rect.x - camera_x
            screen_y = item.rect.y - camera_y
            viewport_surface.blit(item.image, (screen_x, screen_y))

        if level.portal:
            level.portal.update()
            draw_x = level.portal.rect.x - camera_x - level.portal.render_offset_x
            draw_y = level.portal.rect.y - camera_y - level.portal.render_offset_y
            viewport_surface.blit(level.portal.image, (draw_x, draw_y))

            if player.rect.colliderect(level.portal.rect):
                level_manager.go_to_next_level()


        for fireball in level.fireball_group:
            screen.blit(fireball.image, fireball.rect)

        # Render musuh dan projectile ke viewport surface
        for enemy in level.enemies:
            enemy.update(level.platforms, player)

            # Gambar musuh ke viewport
            viewport_surface.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y - camera_y))

            # Update dan gambar semua projectile dari musuh (misal goblin archer)
            if hasattr(enemy, "projectiles"):
                enemy.projectiles.update()
                for proj in enemy.projectiles:
                    # Gambar panah ke viewport sesuai kamera
                    viewport_surface.blit(proj.image, (proj.rect.x - camera_x, proj.rect.y - camera_y))

                    # Cek tabrakan dengan player
                    if proj.rect.colliderect(player.rect):
                        if player.parrying:
                            proj.kill()
                            print("🛡️ Parry berhasil!")
                        else:
                            proj.kill()
                            player.take_damage()
                            print("💥 Player terkena panah!")
                            
        # Render player ke viewport surface
        player.draw(viewport_surface, camera_x, camera_y)

        # Render boss ke viewport surface
        for boss in boss_group:
            viewport_surface.blit(boss.image, (boss.rect.x - camera_x, boss.rect.y - camera_y))

        # Cek apakah boss telah kalah
        if level.level_number == 6 and level.boss_spawned and not boss_defeated:
            all_boss_dead = all(
                isinstance(e, BossSaman) and hasattr(e, "alive") and not e.alive
                for e in level.enemies
                if isinstance(e, BossSaman)
            )
            if all_boss_dead:
                boss_defeated = True
                print("🎉 Semua boss kalah, menampilkan UI Victory!")
                stop_music()
                choice = show_victory_menu()
                if choice == "victory_main_menu":
                    stop_music()
                    boss_defeated = False  # reset untuk sesi baru
                    while True:
                        selected_level = show_main_menu()
                        if isinstance(selected_level, int):
                            break

                    level = Level(selected_level, None, assets)
                    player = Player(
                        100, 400, level.enemies,
                        assets['idle'],
                        assets['walk_right'],
                        assets['walk_left'],
                        assets['jump'],
                        assets['attack'],
                        assets['hurt'],
                        platforms=level.platforms,
                        assets=assets
                    )
                    player.parry_frames = assets['parry']
                    player.death_frames = assets["death"]

                    level.player = player
                    player.items = level.items
                    level_manager.current_level = selected_level
                    level_manager.level = level
                    update_max_width()
                    play_music("Backsound/Level Song.mp3")
                    continue

        # Bersihkan layar utama
        screen.fill((0, 0, 0))  # latar hitam

        # Scale viewport
        scaled_surface = pygame.transform.scale(viewport_surface, (WIDTH, HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        # Render UI biasa (langsung di screen, tanpa scaling)
        draw_text(f"Level: {level.level_number}", 10, 10)

        # Menampilkan health bar
        health_bar_frames = assets["health_bar"]
        if player.shield_hits > 0:
            frame = health_bar_frames[6]  # frame khusus shield
        else:
            frame = health_bar_frames[5 - max(0, min(player.lives, 5))]

        screen.blit(frame, (10, 10))

        if level_manager.current_level != level.level_number:
            level = level_manager.level
            player.enemies = level.enemies

        # Respawn jika jatuh
        if player.rect.y > HEIGHT + 200:
            player.take_damage()
            if player.lives <= 0:
                game_over = True
            else:
                print("😵 Player jatuh! Respawn...")
                spawn_y = find_spawn_y(level.platforms, spawn_x, player.rect.height)
                player.reset(x=spawn_x, y=spawn_y, platforms=level.platforms)

    elif paused:
        choice = show_pause_menu()
        if choice == "continue":
            paused = False
        elif choice == "menu":
            stop_music()
            while True:
                selected_level = show_main_menu()
                if isinstance(selected_level, int):
                    break

            level = Level(selected_level, None, assets)
            player = Player(
                100, 400, level.enemies,
                assets['idle'],
                assets['walk_right'],
                assets['walk_left'],
                assets['jump'],
                assets['attack'],
                assets['hurt'],
                platforms=level.platforms,
                assets=assets
            )
            player.parry_frames = assets['parry']
            player.death_frames = assets["death"]

            level.player = player
            player.items = level.items
            level_manager = LevelManager(player, assets)
            level_manager.current_level = selected_level
            level_manager.level = level
            update_max_width()
            play_music("Backsound/Level Song.mp3")
            paused = False

    elif game_over:
        choice = game_over_menu()
        if choice == "retry":
            level = Level(level_manager.current_level, None, assets)
            player = Player(
                100, 400, level.enemies,
                assets['idle'],
                assets['walk_right'],
                assets['walk_left'],
                assets['jump'],
                assets['attack'],
                assets['hurt'],
                platforms=level.platforms,
                assets=assets,
            )
            player.parry_frames = assets['parry']
            player.death_frames = assets["death"]

            level.player = player
            player.items = level.items
            level_manager.level = level
            update_max_width()
            game_over = False
        elif choice == "exit":
            selected_level = show_main_menu()
            level = Level(selected_level, None, assets)

            player = Player(
                100, 400, level.enemies,
                assets['idle'],
                assets['walk_right'],
                assets['walk_left'],
                assets['jump'],
                assets['attack'],
                assets['hurt']
            )
            player.parry_frames = assets['parry']
            player.death_frames = assets["death"]

            level.player = player
            player.items = level.items
            level_manager.current_level = selected_level
            level_manager.level = level
            update_max_width()
            game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
