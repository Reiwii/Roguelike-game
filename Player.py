import pygame
import pygame.sprite as sprite
from sympy import Integer

class Player(sprite.Sprite):
    def __init__(self,group:sprite.Group):
        super().__init__(group)
        image = pygame.image.load("assets/tile_0098.png").convert_alpha()
        self.image=pygame.transform.scale_by(image,3)
        self.pos = pygame.math.Vector2(500,500)
        self.rect = self.image.get_rect(topleft=self.pos.xy)
        self.mov_speed = 5
    def update(self):
        input_vector = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_w]:
            input_vector.y -= 1
        if keys[pygame.K_s]:
            input_vector.y += 1
        if input_vector.length() > 0:
            input_vector = input_vector.normalize()
            
        self.pos.x += input_vector.x * self.mov_speed
        self.pos.y += input_vector.y * self.mov_speed
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)