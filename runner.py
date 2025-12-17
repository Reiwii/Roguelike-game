import pygame
import Enemy
import Player  
import Camera
import Tree
import random

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

camera = Camera.Camera()
player = Player.Player(camera)
enemy = Enemy.Enemy(player)
camera.add(enemy)

for i in range(100):
    x= random.randint(-4000,4000)
    y= random.randint(0,1000)
    tree = Tree.Tree((x,y),camera)
    
enemies_group = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update()
    for sprite in camera.sprites():
        if hasattr(sprite, 'update') and sprite != player:
            sprite.update(player)
    camera.custom_draw(player)
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()