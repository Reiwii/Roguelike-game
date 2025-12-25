import pygame
import random


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.pos = pygame.math.Vector2(pos)

        self.image = pygame.Surface((24, 18), pygame.SRCALPHA)
        self.image.fill((180, 120, 40))
        pygame.draw.rect(self.image, (80, 50, 20), self.image.get_rect(), 2)

        self.rect = self.image.get_rect(center=self.pos)

