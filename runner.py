import pygame
import Player  
import Camera
import World
from weapons.weapons_from_json import load_weapon_db,create_weapon

#init
pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Camera Movement Example")
clock = pygame.time.Clock()
running = True
dt = 0

enemies_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
all_sprites_group = pygame.sprite.Group()
camera = Camera.Camera()
player = Player.Player(camera,all_sprites_group)
world = World.World(screen,player,camera,enemies_group,all_sprites_group,projectile_group)

weapon_db = load_weapon_db("weapons/weapons.JSON")
magic_wand = create_weapon("magic_wand", weapon_db)
player.weapons.append(magic_wand)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    world.update(dt,camera)
    camera.custom_draw(player)
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    print(clock.get_fps())

pygame.quit()