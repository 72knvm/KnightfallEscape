import os
import pygame

def load_animation_frames(sheet, row, num_frames, frame_width, frame_height, scale=2):
    frames = []
    target_width = frame_width * scale
    target_height = frame_height * scale

    for i in range(num_frames):
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (i * frame_width, row * frame_height, frame_width, frame_height))

        trim_rect = frame.get_bounding_rect()
        trimmed = frame.subsurface(trim_rect).copy()

        stable_frame = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
        scaled_trimmed = pygame.transform.scale(trimmed, (trim_rect.width * scale, trim_rect.height * scale))

        offset_x = (target_width - scaled_trimmed.get_width()) // 2
        offset_y = (target_height - scaled_trimmed.get_height()) // 2
        stable_frame.blit(scaled_trimmed, (offset_x, offset_y))

        frames.append(stable_frame)

    return frames

def load_knight_idle_frames(sprite_sheet, num_frames=7, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_knight_walk_frames(sprite_sheet, num_frames=8, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_knight_jump_frames(sprite_sheet, num_frames=5, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_knight_attack_frames(sprite_sheet, num_frames=6, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_knight_hurt_frames(sprite_sheet, num_frames=4, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_knight_parry_frames(sprite_sheet, num_frames=6, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_knight_death_frames(sprite_sheet, num_frames=12, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_portal_frames(sprite_sheet, num_frames=7, scale_factor=2):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frame = pygame.transform.scale(frame, (frame_width * scale_factor, sheet_height * scale_factor))
        frames.append(frame)
    return frames

def load_health_bar_frames(sprite_sheet, num_frames=6):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    frame_width = sheet_width // num_frames
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, sheet_height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, sheet_height))
        frames.append(frame)
    return frames

def load_archer_frames(sheet, frame_width, frame_height, scale=2):
    animations = {}
    animations["idle"] = load_animation_frames(sheet, row=0, num_frames=5, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["attack"] = load_animation_frames(sheet, row=1, num_frames=11, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["walk"] = load_animation_frames(sheet, row=2, num_frames=8, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["hurt"] = load_animation_frames(sheet, row=3, num_frames=5, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["dead"] = load_animation_frames(sheet, row=4, num_frames=6, frame_width=frame_width, frame_height=frame_height, scale=scale)
    return animations

def load_assets():
    base_path = os.path.dirname(os.path.abspath(__file__))

    def load_sheet(path):
        return pygame.image.load(os.path.join(base_path, "asset", path)).convert_alpha()
    
    heart_path = os.path.join(base_path, "asset", "heart.png")
    heart_sheet = pygame.image.load(heart_path).convert_alpha()
    health_bar_frames = load_health_bar_frames(heart_sheet)

    main_menu_path = os.path.join(base_path, "asset", "main_menu.jpg")
    main_menu_image = pygame.image.load(main_menu_path).convert()

    level_bg_path = os.path.join(base_path, "asset", "Castle_Background.jpg")
    level_bg_image = pygame.image.load(level_bg_path).convert()

    platform_path = os.path.join(base_path, "asset", "platform.png")
    platform_image = pygame.image.load(platform_path).convert_alpha()

    # Idle
    knight_idle_path = os.path.join(base_path, "asset", "IDLE.png")
    knight_idle_sheet = pygame.image.load(knight_idle_path).convert_alpha()
    knight_idle_frames = load_knight_idle_frames(knight_idle_sheet)

    # Walk
    knight_walk_path = os.path.join(base_path, "asset", "WALK.png")
    knight_walk_sheet = pygame.image.load(knight_walk_path).convert_alpha()
    knight_walk_frames = load_knight_walk_frames(knight_walk_sheet)
    knight_walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in knight_walk_frames]

    # Jump
    knight_jump_path = os.path.join(base_path, "asset", "JUMP.png")
    knight_jump_sheet = pygame.image.load(knight_jump_path).convert_alpha()
    knight_jump_frames = load_knight_jump_frames(knight_jump_sheet)

    # Attack
    attack_path = os.path.join(base_path, "asset", "ATTACK.png")
    attack_sheet = pygame.image.load(attack_path).convert_alpha()
    knight_attack_frames = load_knight_attack_frames(attack_sheet)

    # Hurt
    knight_hurt_path = os.path.join(base_path, "asset", "HURT.png")
    knight_hurt_sheet = pygame.image.load(knight_hurt_path).convert_alpha()
    knight_hurt_frames = load_knight_hurt_frames(knight_hurt_sheet, num_frames=4)

    # Parry (Defend)
    parry_path = os.path.join(base_path, "asset", "DEFEND.png")
    parry_sheet = pygame.image.load(parry_path).convert_alpha()
    knight_parry_frames = load_knight_parry_frames(parry_sheet, num_frames=6)

    # Death
    death_path = os.path.join(base_path, "asset", "DEATH.png")
    death_sheet = pygame.image.load(death_path).convert_alpha()
    knight_death_frames = load_knight_death_frames(death_sheet, num_frames=12)

    # Portal
    portal_path = os.path.join(base_path, "asset", "PORTAL.png")
    portal_sheet = pygame.image.load(portal_path).convert_alpha()
    portal_frames = load_portal_frames(portal_sheet)

    # Potion images
    health_potion_path = os.path.join(base_path, "asset", "health_potion.png")
    shield_potion_path = os.path.join(base_path, "asset", "shield_potion.png")

    health_potion_img = pygame.image.load(health_potion_path).convert_alpha()
    shield_potion_img = pygame.image.load(shield_potion_path).convert_alpha()

    # Archer Enemy Sprite Sheet
    archer_path = os.path.join(base_path, "asset", "Arch.png")
    archer_sheet = pygame.image.load(archer_path).convert_alpha()
    archer_frames = load_archer_frames(archer_sheet, frame_width=128, frame_height=128, scale=1)

    # === Goblin Knight Animations (pakai load_animation_frames) ===
    goblin_knight = {}

    # Idle
    idle_path = os.path.join(base_path, "asset", "idle_gk.png")
    idle_sheet = pygame.image.load(idle_path).convert_alpha()
    frame_width = idle_sheet.get_width() // 9
    frame_height = idle_sheet.get_height()
    goblin_knight["idle"] = load_animation_frames(idle_sheet, row=0, num_frames=9, frame_width=frame_width, frame_height=frame_height, scale=1.0)

    # Walk
    walk_path = os.path.join(base_path, "asset", "walk_gk.png")
    walk_sheet = pygame.image.load(walk_path).convert_alpha()
    fw = walk_sheet.get_width() // 9
    fh = walk_sheet.get_height()
    goblin_knight["walk"] = load_animation_frames(walk_sheet, row=0, num_frames=9, frame_width=fw, frame_height=fh, scale=1.0)

    # Hurt
    hurt_path = os.path.join(base_path, "asset", "hurt_gk.png")
    hurt_sheet = pygame.image.load(hurt_path).convert_alpha()
    fw = hurt_sheet.get_width() // 5
    fh = hurt_sheet.get_height()
    goblin_knight["hurt"] = load_animation_frames(hurt_sheet, row=0, num_frames=5, frame_width=fw, frame_height=fh, scale=1.0)

    # Dead
    die_path = os.path.join(base_path, "asset", "die_gk.png")
    die_sheet = pygame.image.load(die_path).convert_alpha()
    fw = die_sheet.get_width() // 10
    fh = die_sheet.get_height()
    goblin_knight["dead"] = load_animation_frames(die_sheet, row=0, num_frames=10, frame_width=fw, frame_height=fh, scale=1.0)

    # Attack
    attack_path = os.path.join(base_path, "asset", "attack_gk.png")
    attack_sheet = pygame.image.load(attack_path).convert_alpha()
    fw = attack_sheet.get_width() // 10
    fh = attack_sheet.get_height()
    goblin_knight["attack"] = load_animation_frames(attack_sheet, row=0, num_frames=10, frame_width=fw, frame_height=fh, scale=1.0)

    # Kembalikan dictionary lengkap
    assets = {
        "health_bar": health_bar_frames,
        "main_menu_bg": main_menu_image,
        "level_bg": level_bg_image,
        "platform": platform_image,
        "idle": knight_idle_frames,
        "walk_right": knight_walk_frames,
        "walk_left": knight_walk_frames_left,
        "jump": knight_jump_frames,
        "attack": knight_attack_frames,
        "hurt": knight_hurt_frames,
        "parry": knight_parry_frames,
        "death": knight_death_frames,
        "portal": portal_frames,
        "health_potion": health_potion_img,
        "shield_potion": shield_potion_img,
        "archer": archer_frames,
        "goblin_knight": goblin_knight,

    }

    return assets

