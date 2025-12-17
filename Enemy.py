import pygame.sprite as sprite
import pygame

class Enemy(sprite.Sprite):
    def __init__(self,pos : tuple[int,int]):
        super().__init__()
        sheet = pygame.image.load("assets/Skeleton.png").convert_alpha()
        self.sheet = pygame.transform.scale_by(sheet,3)
        frame_w = 32 * 3
        frame_h = 32 * 3

        self.frames = self.slice_sheet(frame_w,frame_h)
        # self.front_walk_frames = self.frames[]
        # self.side_walk_frames = self.frames[]
        # self.back_walk_frames = self.frames[]
        # self.die_frames = self.frames[]
        
        
        
        self.frame_index = 0;
        self.pos = pos
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(100,100))
        

    def slice_sheet(self,frame_w: int,frame_h: int) -> list[pygame.Surface]:
        sheet_w,sheet_h = self.sheet.get_size()
        frames = []
        for x in range(0,sheet_w,frame_w):
            for y in range(0,sheet_h,frame_h):
                rect = pygame.Rect(x,y,frame_w,frame_h)
                frame = self.sheet.subsurface(rect).copy()
                frames.append(frame)
        return frames
    def update(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.image = self.frames[self.frame_index]

    