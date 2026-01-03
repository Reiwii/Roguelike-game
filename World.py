# World.py
import pygame
import random
import Player
import Enemy
import Camera
import Tree
import math
from Projectile import LinearProjectile,SlashHitbox,ShurikenProjectile
from collections import defaultdict
from weapons.weapons_from_json import load_weapon_db, create_weapon

class World:
    def __init__(self, screen, player, camera_group,
                 enemies_group, all_sprites_group, projectile_group,exp_orb_group,chest_group):
        self.screen = screen

        self.enemies_group = enemies_group
        self.all_sprites_group = all_sprites_group
        self.projectile_group = projectile_group
        self.camera_group = camera_group
        self.exp_orb_group = exp_orb_group
        self.chest_group = chest_group

        self.player = player
        self.despawn_rect = pygame.Rect(self.player.pos.x,self.player.pos.y,self.screen.get_size()[0],self.screen.get_size()[1])
        self.despawn_rect.inflate_ip(500,500)

        self.start_time = pygame.time.get_ticks()
        self.last_spawn_time = self.start_time
        self.enemies_killed = 0
        self.max_enemies = 300
        self.current_enemies = 0

        self.base_spawn_interval = 2000   
        self.min_spawn_interval  = 1000    
        self.margin              = 150    
        self.number_of_spawned_waves = 0

        for i in range(100):
            x = random.randint(-4000, 4000)
            y = random.randint(0, 1000)
            tree = Tree.Tree((x, y), self.camera_group)
        
        
        self.cell_size = 12
        self.enemy_grid = defaultdict(list)

        self.weapon_db = load_weapon_db("weapons/weapons.JSON")
        self.all_weapon_ids = list(self.weapon_db.keys())

        #load images
        self.assets = {}
        self.assets["magic_wand"] = self.load_image("assets/weapons/magic_wand/magic_wand.png",1.5)
        self.assets["sword"] = self.load_image("assets/weapons/sword/sword.png",1.5)
        self.assets["crossbow"] = self.load_image("assets/weapons/crossbow/crossbow.png",1.5)
        self.assets["shuriken"] = self.load_image("assets/weapons/shuriken/shuriken.png",1.5)
        self.anims = {}
        self.anims["sword"] = self.load_image("assets/weapons/sword/projectile/slash6.png",)
        self.anims["arrow"] = self.load_image("assets/weapons/crossbow/arrow.png")
        self.anims["shuriken"] = self.load_image("assets/weapons/shuriken/shuriken.png",1.5)
        

    def rebuild_enemy_grid(self):
        self.enemy_grid.clear()
        cs = self.cell_size
        for e in self.enemies_group:
            self.enemy_grid[(int(e.pos.x // cs), int(e.pos.y // cs))].append(e)

    def resolve_enemy_collisions(self):
        for (cx, cy), enemies in self.enemy_grid.items():
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    neighbors = self.enemy_grid.get((cx + dx, cy + dy), [])
                    for a in enemies:
                        for b in neighbors:
                            if a is b or id(a) >= id(b):
                                continue
                            delta = a.pos - b.pos
                            d2 = delta.length_squared()
                            if d2 == 0:
                                continue
                            min_dist = a.radius + b.radius
                            if d2 < min_dist * min_dist:
                                dist = d2 ** 0.5
                                overlap = (min_dist - dist)
                                push = overlap * 0.2      
                                delta.scale_to_length(push * 0.5)
                                a.pos += delta
                                b.pos -= delta


    def register_enemy_kill(self):
        self.enemies_killed += 1

    def get_spawn_interval_ms(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
        difficulty = 1.0 + elapsed * 0.01 + self.enemies_killed * 0.02
        interval = self.base_spawn_interval / difficulty
        return max(interval, self.min_spawn_interval)

    def get_batch_size(self):
        return 1 + self.enemies_killed // 20

    def random_pos_outside_camera(self, camera):
        angle = random.random() * 2 * math.pi          
        dist  = random.randint(400,800)    

        x = self.player.rect.centerx + math.cos(angle) * dist
        y = self.player.rect.centery + math.sin(angle) * dist

        return x, y


    def spawn_enemies(self, camera):
        if self.max_enemies <= self.current_enemies:
            return

        now = pygame.time.get_ticks()
        interval = self.get_spawn_interval_ms()
        if now - self.last_spawn_time < interval:
            return

        self.number_of_spawned_waves +=1
        if self.number_of_spawned_waves % 2 == 0:
            x, y = self.random_pos_outside_camera(camera)
            Enemy.Enemy((x, y),True, self.camera_group,
                        self.enemies_group, self.all_sprites_group)

        self.last_spawn_time = now
        batch = self.get_batch_size()
        self.current_enemies += batch
        for _ in range(batch):
            x, y = self.random_pos_outside_camera(camera)
            Enemy.Enemy((x, y),False, self.camera_group,
                        self.enemies_group, self.all_sprites_group)

    def update(self, dt, camera):
        self.despawn_rect.center = self.player.pos
        self.all_sprites_group.update(self, dt)
        self.spawn_enemies(camera)
        self.rebuild_enemy_grid()
        self.resolve_enemy_collisions()

        #gem orb 
        gems_hit = pygame.sprite.spritecollide(self.player, self.exp_orb_group, dokill=True)
        for gem in gems_hit:
            self.player.add_xp(gem.value)
            gem.kill()

        #chest 
        opened = pygame.sprite.spritecollide(self.player, self.chest_group, dokill=True)
        for chest in opened:
            self.open_chest()


        #PLAYER ENEMY COL
        hits = pygame.sprite.spritecollide(
            self.player,
            self.enemies_group,
            dokill=False,
            collided=pygame.sprite.collide_circle)

        for e in hits:
            self.player.take_damage(e.stats.damage)
            e.take_damage(0,self,self.player.pos)

        for e in self.enemies_group:
            if not self.despawn_rect.colliderect(e.rect):
                x, y = self.random_pos_outside_camera(camera)
                e.pos.update(x, y)
                e.rect.center = (int(x), int(y))



    def spawn_projectile(self,  projectile_id, pos, vel=(0,0), damage=1, pierce=1, owner=None, radius=3, lifetime=0.1,bounces=0):
        if projectile_id == "arrow":
            img = self.anims["arrow"]  
            LinearProjectile(pos, vel, damage, pierce, owner, img, radius, self.projectile_group, self.all_sprites_group, self.camera_group)

        elif projectile_id == "slash":
            img = self.anims["sword"]  
            SlashHitbox(owner, damage, pierce, radius, img, lifetime, self.projectile_group, self.all_sprites_group, self.camera_group)
        elif projectile_id == "shuriken":
            img = self.assets["shuriken"]
            ShurikenProjectile(pos, vel, damage, pierce, owner, img, radius,
                      self.projectile_group, self.all_sprites_group, self.camera_group)



    def open_chest(self):
        upgradable = [w for w in self.player.weapons if w.can_level_up()]
        if not upgradable:
            return
        w = random.choice(upgradable)
        w.level_up()

    def load_image(self,path, scale=None):
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale_by(img, scale)
        return img