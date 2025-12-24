import pygame
import pygame.sprite as sprite
import World
from dataclasses import dataclass
from weapons.Base import BaseWeapon

@dataclass(slots=True)
class PlayerCombatStats:
    might_mult: float = 1.0          
    cooldown_mult: float = 1.0      
    area_mult: float = 1.0
    duration_mult: float = 1.0
    speed_mult: float = 1.0
    amount_bonus: int = 0           
    pierce_bonus: int = 0

class Player(sprite.Sprite):
    def __init__(self,*group:list[sprite.Group]):
        super().__init__(*group)
        image = pygame.image.load("assets/tile_0098.png").convert_alpha()
        self.image=pygame.transform.scale_by(image,3)
        self.pos = pygame.math.Vector2(500,500)
        self.rect = self.image.get_rect(center=self.pos)
        self.radius = 10 
        self.speed = 2 

        self.combat_stats = PlayerCombatStats()
        self.weapons: list[BaseWeapon] = [] 

    def update(self,world:World,dt):
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
            
        self.pos.x += input_vector.x * self.speed 
        self.pos.y += input_vector.y * self.speed 
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

        for w in self.weapons:
            w.update(dt, world, self)