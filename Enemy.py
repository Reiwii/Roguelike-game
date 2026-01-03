import pygame.sprite as sprite
import pygame
import World
import weapons.Base as Base
from dataclasses import dataclass
import ExpGem
from Chest import Chest

@dataclass
class EnemyStats:
    hp: int
    damage: int
    speed: int

class Enemy(sprite.Sprite):
    sheet = None
    frames = None
    animations = None
    def __init__(self,pos,is_boss,*groups:list[pygame.sprite.Group]):
        super().__init__(*groups)
    
        # combat stats 
        self.is_boss=is_boss
        if self.is_boss:
            self.stats = EnemyStats(10,10,1)
            self.radius = 32
            self.scale = 2
        else:
            self.stats = EnemyStats(20,10,1)
            self.radius = 16
            self.scale = 1

        self.load_animations()
        self.action = 'walk_side_left' 
        self.frame_index = 0;
        self.pos = pygame.math.Vector2(pos)
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=self.pos)
        self.frame_count = 0;
        self.animation_speed = 0.05;
        self.knockback = pygame.math.Vector2()
        self.knockback_decay = 5     
        self.max_knockback = 450


        
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

        self.pos += self.knockback * dt
        self.knockback -= self.knockback * self.knockback_decay * dt
        if self.knockback.length_squared() < 1:
            self.knockback.update(0, 0)


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
        frame = animation_list[self.frame_index]
        self.image = pygame.transform.scale_by(frame,self.scale)



    def set_action(self,action:str)->None:
        self.action = action
        return None


    def take_damage(self, amount: int, world, source_pos, knockback=250):
        if self.action == "die":
            return

        self.stats.hp -= amount

        if source_pos is not None:
            d = self.pos - pygame.math.Vector2(source_pos)
            if d.length_squared() > 0:
                d = d.normalize()
                self.knockback += d * knockback
                if self.knockback.length() > self.max_knockback:
                    self.knockback.scale_to_length(self.max_knockback)

        if self.stats.hp <= 0:
            world.register_enemy_kill()
            world.current_enemies -= 1
            self.stats.hp = 0
            self.action = "die"
            self.frame_index = 0
            self.frame_count = 0

            if self.is_boss:
                Chest(self.pos, world.chest_group, world.all_sprites_group, world.camera_group)
            else:
                ExpGem.ExpGem(self.pos, world.exp_orb_group, world.all_sprites_group, world.camera_group)

