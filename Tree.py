import pygame

class Tree(pygame.sprite.Sprite):
    def __init__(self,pos, group):
        super().__init__(group)
        image = pygame.image.load("assets/tree.png").convert_alpha()
        self.image = pygame.transform.scale_by(image,4)
        self.rect = self.image.get_rect(topleft=pos)