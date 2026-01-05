import pygame
import math

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface =  pygame.display.get_surface()
        self.screen_width = self.display_surface.get_size()[0]
        self.screen_height = self.display_surface.get_size()[1]
        self.offset = pygame.math.Vector2()

        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.screen_width - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.screen_height - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

        ground_surf = pygame.image.load('assets/map.png').convert_alpha()
        self.ground_surf = pygame.transform.scale_by(ground_surf,3)
        self.ground_rect = self.ground_surf.get_rect()
        self.ground_width = self.ground_rect.width
        self.tiles = math.ceil(self.screen_width / self.ground_width)


    def on_resize(self, screen):
        self.display_surface = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.display_surface.get_size()

        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.screen_width - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.screen_height - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        self.tiles = math.ceil(self.screen_width / self.ground_width)
    def box_target_camera(self,target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom
        min_top = self.ground_rect.top + self.camera_borders['top']
        if self.camera_rect.top < min_top:
            self.camera_rect.top = min_top
            
        max_bottom = self.ground_rect.bottom - self.camera_borders['bottom']
        if self.camera_rect.bottom > max_bottom:
            self.camera_rect.bottom = max_bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self,player):
        self.box_target_camera(player)
        start_col = int(self.offset.x // self.ground_width)
        for x in range(start_col - 1, start_col + self.tiles + 2):
            x_pos = (x * self.ground_width) - self.offset.x
            y_pos = self.ground_rect.top - self.offset.y
            self.display_surface.blit(self.ground_surf, (x_pos, y_pos))

        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset 
            self.display_surface.blit(sprite.image,offset_pos)

