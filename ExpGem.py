import pygame

class ExpGem(pygame.sprite.Sprite):
    def __init__(self,pos,image, *groups):
        super().__init__(*groups)
        self.value = 1
        self.pos = pos
        self.image = image 
        self.rect = self.image.get_rect(center=self.pos)