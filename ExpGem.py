import pygame

class ExpGem(pygame.sprite.Sprite):
    def __init__(self,pos, *groups):
        super().__init__(*groups)
        self.value = 1
        self.pos = pos
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)