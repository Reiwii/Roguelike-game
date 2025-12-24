import pygame.sprite as sprite
import pygame
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
    sheet = None
    frames = None
    animations = None
    def __init__(self,pos,*groups:list[pygame.sprite.Group]):
        super().__init__(*groups)
    
        # combat stats 
        self.stats = EnemyStats(100,100,10,1)
        self.dead = False

        self.load_animations()
        self.action = 'walk_side_left' 
        self.frame_index = 0;
        self.pos = pygame.math.Vector2(pos)
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=self.pos)
        self.radius = 16
        self.frame_count = 0;
        self.animation_speed = 0.05;

        
    @classmethod
    def load_animations(cls):
        if cls.sheet is not None:
            return
        sheet = pygame.image.load("assets/Skeleton.png").convert_alpha()
        cls.sheet = pygame.transform.scale_by(sheet,3)
        frame_w = 32 * 3
        frame_h = 32 * 3
        cls.all_frames = cls.slice_sheet(cls.sheet,frame_w,frame_h)
        for i,frame in enumerate(cls.all_frames[24:30]):
            cls.all_frames[i] = pygame.transform.flip(frame,flip_x=True,flip_y=False)

        cls.animations = {
            'walk_side_right':cls.all_frames[24:30],
            'walk_side_left':cls.all_frames[0:6],
            'die':cls.all_frames[36:40]
        }
            
        
    @staticmethod
    def slice_sheet(sheet,frame_w: int,frame_h: int) -> list[pygame.Surface]:
        sheet_w,sheet_h = sheet.get_size()
        frames = []
        for y in range(0,sheet_h,frame_h):
            for x in range(0,sheet_w,frame_w):
                rect = pygame.Rect(x,y,frame_w,frame_h)
                frame = sheet.subsurface(rect).copy()
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



    def set_action(self,action:str)->None:
        self.action = action
        return None


    def take_damage(self, amount: int,world):
        if self.action=="die":
            return
        self.stats.hp -= amount
        if self.stats.hp <= 0:
            world.register_enemy_kill()
            world.current_enemies -= 1
            self.stats.hp = 0
            self.action = "die"
            self.frame_index = 0
            self.frame_count = 0 