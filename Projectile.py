import pygame

class DamageHitbox(pygame.sprite.Sprite):
    def __init__(self, pos, damage, pierce, owner, image, *groups):
        super().__init__(*groups)
        self.owner = owner
        self.pos = pygame.Vector2(pos)

        self.damage = damage
        self.pierce = pierce          #-1 inf
        self.enemies_hit = set()

        self.image = image
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

    def on_hit_enemy(self, world, enemy):
        enemy.take_damage(self.damage, world, world.player.pos)

    def handle_hits(self, world):
        for e in world.enemies_near(self.pos,self.radius):
            if e.action == "die" or e in self.enemies_hit:
                continue

            if not pygame.sprite.collide_circle(self, e):
                continue  

            self.enemies_hit.add(e)
            self.on_hit_enemy(world, e)

            if self.pierce > 0: 
                self.pierce -= 1
                if self.pierce <= 0:
                    self.kill()
                    return


class LinearProjectile(DamageHitbox):
    def __init__(self, pos, vel, damage, pierce, owner, image,  *groups):
        self.vel = pygame.Vector2(vel)
        self.original_image = image
        super().__init__(pos, damage, pierce, owner, image, *groups)
        self.radius = 6


        if self.vel.length_squared() > 0:
            angle = self.vel.angle_to(pygame.math.Vector2(1,0)) - 45
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)


    def update(self, world, dt):
        if not world.despawn_rect.colliderect(self.rect):
            self.kill()
            return

        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.handle_hits(world)
        


class SlashHitbox(DamageHitbox):
    def __init__(self, owner, damage, pierce, image, lifetime, *groups):
        super().__init__(owner.rect.center, damage, pierce, owner, image, *groups)
        self.lifetime = lifetime
        self.radius = 100

    def update(self, world, dt):
        self.pos.update(self.owner.rect.center)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        self.handle_hits(world)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
class ShurikenProjectile(DamageHitbox):
    def __init__(self, pos, vel, damage, pierce, owner, image, *groups):
        self.vel = pygame.Vector2(vel)
        super().__init__(pos, damage, pierce, owner, image, *groups)
        self.radius = 6

    def on_hit_enemy(self, world, enemy):
        enemy.take_damage(self.damage, world, world.player.pos)
        self.vel *= -1
        self.enemies_hit.clear()

    def handle_hits(self, world):
        hits = pygame.sprite.spritecollide(
            self, world.enemies_group, False, collided=pygame.sprite.collide_circle
        )
        for e in hits:
            if e.action == "die" or e in self.enemies_hit:
                continue

            self.enemies_hit.add(e)
            self.on_hit_enemy(world, e)

            self.pierce -= 1
            if self.pierce <= 0:
                self.kill()
            break  

    def update(self, world, dt):
        if not world.despawn_rect.colliderect(self.rect):
            self.kill()
            return

        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.handle_hits(world)
