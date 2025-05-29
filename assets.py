import os
import pygame

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

def load_assets():
    base_path = os.path.dirname(os.path.abspath(__file__))

    heart_path = os.path.join(base_path, "asset", "heart.png")
    heart_image = pygame.image.load(heart_path).convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (32, 32))

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

    # Kembalikan dictionary lengkap
    assets = {
        "heart": heart_image,
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

    }

    return assets

