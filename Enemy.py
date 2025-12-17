from narwhals import String
import pygame.sprite as sprite
import pygame
import random

class Enemy(sprite.Sprite):
    def __init__(self,target:sprite.Sprite):
        super().__init__()

        #Animation
        sheet = pygame.image.load("assets/Skeleton.png").convert_alpha()
        self.sheet = pygame.transform.scale_by(sheet,3)
        frame_w = 32 * 3
        frame_h = 32 * 3
        self.all_frames = self.slice_sheet(frame_w,frame_h)
        self.animations = {
            'stand':      self.all_frames[0:6],
            'walk_front': self.all_frames[18:24],
            'walk_side':  self.all_frames[24:30],
            'walk_back':  self.all_frames[30:36],
            'die':        self.all_frames[36:40]
        }
        self.frame_index = 0;

        
        self.target = target
        x= random.gauss(target.rect.topleft[0],100)
        y= random.gauss(target.rect.topleft[1],100)
        self.pos = pygame.math.Vector2(x,y)
        self.image = self.all_frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=self.pos.xy)
        self.action = 'stand' 
        self.frame_count = 0;
        self.animation_speed = 0.05;
        self.mov_speed = 3

        

    def slice_sheet(self,frame_w: int,frame_h: int) -> list[pygame.Surface]:
        sheet_w,sheet_h = self.sheet.get_size()
        frames = []
        for y in range(0,sheet_h,frame_h):
            for x in range(0,sheet_w,frame_w):
                rect = pygame.Rect(x,y,frame_w,frame_h)
                frame = self.sheet.subsurface(rect).copy()
                frames.append(frame)
        return frames

    def update(self,target:sprite.Sprite):
        direction_vector = pygame.math.Vector2()
        direction_vector.x = target.pos.x - self.pos.x
        direction_vector.y = target.pos.y - self.pos.y
        distance = direction_vector.length()
        direction_vector.normalize_ip()
        if distance > 2:
            self.pos.x += direction_vector.x * self.mov_speed
            self.pos.y += direction_vector.y * self.mov_speed

        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

        self.animate()

    
    
    def animate(self):
        self.frame_count += self.animation_speed
        animation_list = self.animations[self.action]

        if self.frame_index >= len(animation_list)-1:
            if self.action == "die":
                self.frame_index = len(animation_list) - 1
            else:
                self.frame_index = 0
        if self.frame_count > 1:
            self.frame_index +=1
            self.frame_count = 0

        self.image = animation_list[self.frame_index]



    def set_action(self,action:String)->None:
        self.action = action
        return None


    