import pygame
import pygame.sprite as sprite

class Player(sprite.Sprite):
    def __init__(self,group):
        super().__init__(group)
        image = pygame.image.load("tile_0098.png").convert_alpha()
        self.image=pygame.transform.scale_by(image,3)
        self.rect = self.image.get_rect(topleft=(500,550))
        self.mov_speed = 4
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
            
        self.rect.center += input_vector * self.mov_speed