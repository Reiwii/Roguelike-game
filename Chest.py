import pygame
import random


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.pos = pygame.math.Vector2(pos)

        image = pygame.image.load("assets/chest.png")
        self.image = pygame.transform.scale_by(image,2)

        self.rect = self.image.get_rect(center=self.pos)

