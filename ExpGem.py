import pygame

class ExpGem(pygame.sprite.Sprite):
    def __init__(self,pos, *groups):
        super().__init__(*groups)
        self.value = 1
        self.pos = pos
        self.image = pygame.image.load("assets/exp_orb.png")
        self.rect = self.image.get_rect(center=self.pos)