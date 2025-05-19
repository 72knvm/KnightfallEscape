import os
import pygame

def load_assets():
    base_path = os.path.dirname(os.path.abspath(__file__))  # folder Knightfall
    heart_path = os.path.join(base_path, "asset", "heart.png")
    heart_image = pygame.image.load(heart_path).convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (32, 32))

    return {
        "heart": heart_image,
    }
