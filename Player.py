import pygame
import pygame.sprite as sprite
import World
from dataclasses import dataclass
from weapons.Base import BaseWeapon

@dataclass
class PlayerCombatStats:
    might_mult: float = 1.0          
    cooldown_mult: float = 1.0      
    speed_mult: float = 1.0
    amount_bonus: int = 0           
    pierce_bonus: int = 0

@dataclass
class Attribute:
    id: str
    level: int = 0
    max_level: int = 5
    def can_level_up(self): return self.level < self.max_level
    def level_up(self):
        if not self.can_level_up():
            return False
        self.level += 1
        return True

class Player(sprite.Sprite):
    def __init__(self,*group:list[sprite.Group]):
        super().__init__(*group)
        image = pygame.image.load("assets/tile_0098.png").convert_alpha()
        self.image=pygame.transform.scale_by(image,3)
        self.pos = pygame.math.Vector2(500,500)
        self.rect = self.image.get_rect(center=self.pos)
        self.radius = 10 
        self.speed = 2 
        self.hp = 100
        self.max_hp = 100

        self.combat_stats = PlayerCombatStats()
        self.weapons: list[BaseWeapon] = [] 
        self.attributes: dict[str,Attribute] = {}
        self.xp = 0
        self.level = 1
        self.leveled_up = False
        self.xp_to_next_level = 10
        self.last_hit_ms = 0
        self.hit_cooldown_ms = 500  


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
        self.rect.centerx = round(self.pos.x)
        
        self.pos.y += input_vector.y * self.speed 
        min_y = world.map_top + world.player_padding_top_y
        max_y = world.map_bottom - world.player_padding_bottom_y
        if self.pos.y < min_y:
            self.pos.y = min_y
        elif self.pos.y > max_y:
            self.pos.y = max_y
        self.rect.centery = round(self.pos.y)

        for w in self.weapons:
            w.update(dt, world, self)
        
    def add_xp(self,value):
        self.xp += value
        if self.xp >= self.xp_to_next_level:
            self.xp = 0
            self.xp_to_next_level += 10 
            self.level +=1
            self.leveled_up = True

            
    def take_damage(self, amount: int):
        now = pygame.time.get_ticks()
        if now - self.last_hit_ms < self.hit_cooldown_ms:
            return
        self.last_hit_ms = now
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            print("die")

    def recalculate_combat_stats(self):
        for attr in self.attributes.values():
            if attr.id == "elixir":
                self.combat_stats.might_mult +=  0.1
            elif attr.id == "hook":
                self.combat_stats.cooldown_mult -=  0.1
            elif attr.id == "ring":
                self.combat_stats.amount_bonus += attr.level
            elif attr.id == "lamp":
                self.combat_stats.pierce_bonus += attr.level
            elif attr.id == "scroll":
                self.combat_stats.speed_mult += 0.1

        self.combat_stats.cooldown_mult = max(0.5, self.combat_stats.cooldown_mult)
        print(self.combat_stats)
