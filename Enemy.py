from narwhals import String
import pygame.sprite as sprite
import pygame
import random
import World
import weapons.Base as Base
from dataclasses import dataclass

@dataclass
class EnemyStats:
    max_hp: int 
    hp: int
    damage: int
    speed: int

class Enemy(sprite.Sprite):
    def __init__(self,pos,*groups:list[pygame.sprite.Group]):
        super().__init__(*groups)
    
        # combat stats 
        self.stats = EnemyStats(100,1,10,1)
        #Animation
        sheet = pygame.image.load("assets/Skeleton.png").convert_alpha()
        self.sheet = pygame.transform.scale_by(sheet,3)
        frame_w = 32 * 3
        frame_h = 32 * 3
        self.all_frames = self.slice_sheet(frame_w,frame_h)
        for i,frame in enumerate(self.all_frames[24:30]):
            self.all_frames[i] = pygame.transform.flip(frame,flip_x=True,flip_y=False)
            
        self.animations = {
            'walk_side_right':  self.all_frames[24:30],
            'walk_side_left':  self.all_frames[0:6],
            'die':        self.all_frames[36:40]
        }
        self.frame_index = 0;
        self.pos = pygame.math.Vector2(pos)
        self.image = self.all_frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=self.pos.xy)
        self.action = 'walk_side_left' 
        self.frame_count = 0;
        self.animation_speed = 0.05;

        

    def slice_sheet(self,frame_w: int,frame_h: int) -> list[pygame.Surface]:
        sheet_w,sheet_h = self.sheet.get_size()
        frames = []
        for y in range(0,sheet_h,frame_h):
            for x in range(0,sheet_w,frame_w):
                rect = pygame.Rect(x,y,frame_w,frame_h)
                frame = self.sheet.subsurface(rect).copy()
                frames.append(frame)
        return frames


    def update(self,world:World,dt):
        if self.action == "die":
            self.animate()
            return
        if world.player.pos.x < self.pos.x:
            self.action = 'walk_side_left'
        else:
            self.action = 'walk_side_right'
        direction_vector = pygame.math.Vector2()
        direction_vector.x = world.player.pos.x - self.pos.x
        direction_vector.y = world.player.pos.y - self.pos.y
        distance = direction_vector.length()
        direction_vector.normalize_ip()
        if distance > 2:
            self.pos.x += direction_vector.x * self.stats.speed
            self.pos.y += direction_vector.y * self.stats.speed

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

        self.animate()

    
    
    def animate(self):
        self.frame_count += self.animation_speed
        animation_list = self.animations[self.action]

        if self.frame_count > 1:
            self.frame_index +=1
            self.frame_count = 0

        if self.frame_index >= len(animation_list)-1:
            if self.action == "die":
                self.kill()
                return
            self.frame_index = 0
            

        self.image = animation_list[self.frame_index]



    def set_action(self,action:String)->None:
        self.action = action
        return None


    def take_damage(self, amount: int):
        if self.action=="die":
            return
        self.stats.hp -= amount
        if self.stats.hp <= 0:
            self.stats.hp = 0
            self.action = "die"
            self.frame_index = 0
            self.frame_count = 0 