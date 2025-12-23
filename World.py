# World.py
import pygame
import random
import Player
import Enemy
import Camera
import Tree
import math
import Projectile

class World:
    def __init__(self, screen, player, camera_group,
                 enemies_group, all_sprites_group, projectile_group):
        self.screen = screen

        self.enemies_group = enemies_group
        self.all_sprites_group = all_sprites_group
        self.projectile_group = projectile_group
        self.camera_group = camera_group

        self.player = player

        self.start_time = pygame.time.get_ticks()
        self.last_spawn_time = self.start_time
        self.enemies_killed = 0

        self.base_spawn_interval = 1000   
        self.min_spawn_interval  = 250    
        self.margin              = 150    


        # trees
        for i in range(100):
            x = random.randint(-4000, 4000)
            y = random.randint(0, 1000)
            tree = Tree.Tree((x, y), self.camera_group)

    def register_enemy_kill(self):
        self.enemies_killed += 1

    def get_spawn_interval_ms(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
        difficulty = 1.0 + elapsed * 0.02 + self.enemies_killed * 0.03
        interval = self.base_spawn_interval / difficulty
        return max(interval, self.min_spawn_interval)

    def get_batch_size(self):
        return 10 + self.enemies_killed // 10

    def random_pos_outside_camera(self, camera):
        angle = random.random() * 2 * math.pi          
        dist  = random.randint(400,800)    

        x = self.player.rect.centerx + math.cos(angle) * dist
        y = self.player.rect.centery + math.sin(angle) * dist

        return x, y


    def spawn_enemies(self, camera):
        now = pygame.time.get_ticks()
        interval = self.get_spawn_interval_ms()
        if now - self.last_spawn_time < interval:
            return

        self.last_spawn_time = now
        batch = self.get_batch_size()
        for _ in range(batch):
            x, y = self.random_pos_outside_camera(camera)
            Enemy.Enemy((x, y), self.camera_group,
                        self.enemies_group, self.all_sprites_group)

    def update(self, dt, camera):
        self.all_sprites_group.update(self, dt)
        self.spawn_enemies(camera)

    def spawn_projectile(self, pos, vel, damage, pierce, owner):
        Projectile.Projectile(
            pos,vel,damage,pierce,owner,
            self.projectile_group, self.all_sprites_group, self.camera_group
        )
