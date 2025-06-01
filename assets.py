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

def load_health_bar_frames(sheet, num_frames=6):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // num_frames
    frame_height = sheet_height // 2  # karena 2 baris

    # Baris 0: health biasa
    for i in range(num_frames):
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)

    # Baris 1: shield
    shield_frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
    shield_frame.blit(sheet, (0, 0), (0, frame_height, frame_width, frame_height))
    frames.append(shield_frame)  # indeks ke-6
    return frames

def load_archer_frames(sheet, frame_width, frame_height, scale=2):
    animations = {}
    animations["idle"] = load_animation_frames(sheet, row=0, num_frames=5, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["attack"] = load_animation_frames(sheet, row=1, num_frames=11, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["walk"] = load_animation_frames(sheet, row=2, num_frames=8, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["hurt"] = load_animation_frames(sheet, row=3, num_frames=5, frame_width=frame_width, frame_height=frame_height, scale=scale)
    animations["dead"] = load_animation_frames(sheet, row=4, num_frames=6, frame_width=frame_width, frame_height=frame_height, scale=scale)
    return animations

def load_sheet_shaman(base_path, name, frame_count):
    path = os.path.join(base_path, "asset", name + ".png")
    sheet = pygame.image.load(path).convert_alpha()
    fw = sheet.get_width() // frame_count
    fh = sheet.get_height()
    return load_animation_frames(sheet, row=0, num_frames=frame_count, frame_width=fw, frame_height=fh, scale=2)

def load_assets():
    base_path = os.path.dirname(os.path.abspath(__file__))

    def load_sheet(path):
        return pygame.image.load(os.path.join(base_path, "asset", path)).convert_alpha()
    
    heart_path = os.path.join(base_path, "asset", "heart.png")
    heart_sheet = pygame.image.load(heart_path).convert_alpha()
    health_bar_frames = load_health_bar_frames(heart_sheet)

    main_menu_path = os.path.join(base_path, "asset", "main_menu.jpg")
    main_menu_image = pygame.image.load(main_menu_path).convert()

    boss_room_path = os.path.join(base_path, "asset", "boss_room.png")
    boss_room_image = pygame.image.load(boss_room_path).convert_alpha()

    level_bg_path = os.path.join(base_path, "asset", "Castle_Background.jpg")
    level_bg_image = pygame.image.load(level_bg_path).convert()

    platform_path = os.path.join(base_path, "asset", "plat_bg.jpg")
    platform_image = pygame.image.load(platform_path).convert_alpha()

    victory_bg_path = os.path.join(base_path, "asset", "victory.png")
    victory_bg = pygame.image.load(victory_bg_path).convert()

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

    # Arrow
    arrow_path = os.path.join(base_path, "asset", "arrow.png")
    arrow_image = pygame.image.load(arrow_path).convert_alpha()

    # Fireball
    fireball_sheet = pygame.image.load(os.path.join(base_path, "asset", "Fireball.png")).convert_alpha()
    fireball_frames = load_animation_frames(fireball_sheet, row=0, num_frames=6, frame_width=32, frame_height=32, scale=1)

    # Sound Effect
    attack_sound_path = os.path.join(base_path, "asset", "attack.ogg")
    attack_sound = pygame.mixer.Sound(attack_sound_path)
    attack_sound.set_volume(0.7)  # 0.0 hingga 1.0

    jump_sound_path = os.path.join(base_path, "asset", "jump.ogg")
    jump_sound = pygame.mixer.Sound(jump_sound_path)
    jump_sound.set_volume(1.0)  # opsional

    hurt_sound_path = os.path.join(base_path, "asset", "hurt.wav")
    hurt_sound = pygame.mixer.Sound(hurt_sound_path)
    hurt_sound.set_volume(1.0)  # opsional

    parry_sound_path = os.path.join(base_path, "asset", "parry.wav")
    parry_sound = pygame.mixer.Sound(parry_sound_path)
    parry_sound.set_volume(1.0)  # opsional

    walk_sound_path = os.path.join(base_path, "asset", "walk.wav")
    walk_sound = pygame.mixer.Sound(walk_sound_path)
    walk_sound.set_volume(1.0)

    dead_sound_path = os.path.join(base_path, "asset", "dead.wav")
    dead_sound = pygame.mixer.Sound(dead_sound_path)
    dead_sound.set_volume(1.0)

    drink_sound_path = os.path.join(base_path, "asset", "drink.wav")
    drink_sound = pygame.mixer.Sound(drink_sound_path)
    drink_sound.set_volume(1.0)

    goblin_death_path = os.path.join(base_path, "asset", "goblin_death.wav")
    goblin_death_sound = pygame.mixer.Sound(goblin_death_path)
    goblin_death_sound.set_volume(1.0)

    hit_goblin_path = os.path.join(base_path, "asset", "hit_goblin.wav")
    hit_goblin_sound = pygame.mixer.Sound(hit_goblin_path)
    hit_goblin_sound.set_volume(1.0)

    arrow_sound_path = os.path.join(base_path, "asset", "arrow.wav")
    arrow_sound = pygame.mixer.Sound(arrow_sound_path)
    arrow_sound.set_volume(1.0)

    slash_goblin_path = os.path.join(base_path, "asset", "slash_goblin.wav")
    slash_goblin_sound = pygame.mixer.Sound(slash_goblin_path)
    slash_goblin_sound.set_volume(1.0)

    fireball_sound_path = os.path.join(base_path, "asset", "fireball.wav")
    fireball_sound = pygame.mixer.Sound(fireball_sound_path)
    fireball_sound.set_volume(1.0)

    summon_path = os.path.join(base_path, "asset", "summon.wav")
    summon_sound = pygame.mixer.Sound(summon_path)
    summon_sound.set_volume(1.0)

    shaman = {
        "idle": load_sheet_shaman(base_path, "Idle_SH", 8),
        "move": load_sheet_shaman(base_path, "Move_SH", 8),
        "attack": load_sheet_shaman(base_path, "Attack_SH", 8),
        "hit": load_sheet_shaman(base_path, "Take Hit_SH", 4),
        "death": load_sheet_shaman(base_path, "Death_SH", 5)
    }

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
        "shaman": shaman,
        "arrow": arrow_image,
        "boss_room_platform": boss_room_image,
        "boss_fireball": fireball_frames,
        "attack_sound": attack_sound,
        "jump_sound": jump_sound,
        "hurt_sound": hurt_sound,
        "parry_sound": parry_sound,
        "walk_sound": walk_sound,
        "dead_sound": dead_sound,
        "drink_sound": drink_sound,
        "goblin_death_sound": goblin_death_sound,
        "hit_goblin_sound": hit_goblin_sound,
        "arrow_sound": arrow_sound,
        "slash_goblin_sound": slash_goblin_sound,
        "fireball_sound": fireball_sound,
        "summond_sound": summon_sound,
        "victory_bg": victory_bg,
    }

    return assets

