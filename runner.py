import pygame
import Player  
import Camera
import Tree
import random

# --- Configuration ---
pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2

# --- Initialize Screen ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Camera Movement Example")
clock = pygame.time.Clock()
running = True
dt = 0

camera = Camera.Camera()
# --- Load Assets ---
player = Player.Player(camera)
for i in range(100):
    x= random.randint(-4000,4000)
    y= random.randint(0,1000)
    tree = Tree.Tree((x,y),camera)
    

# --- Groups ---
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# --- Game Loop ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    camera.update()
    camera.custom_draw(player)


    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()