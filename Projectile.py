import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, vel, damage, pierce, owner, *groups):
        super().__init__(*groups)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.damage = damage
        self.pierce = pierce
        self.owner = owner
        self.radius = 3
        self.pierce = 2
        self.enemies_hit: set[pygame.sprite.Sprite] = set()
        self.lifetime = 1.0
        self.age = 0

        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, world, dt):
        self.age += dt
        if self.age > self.lifetime:
            self.kill()
        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        hits = pygame.sprite.spritecollide(self, world.enemies_group, False,collided=pygame.sprite.collide_circle)

        for e in hits:
            if e in self.enemies_hit:
                continue
            self.enemies_hit.add(e)
            e.take_damage(self.damage,world)
            self.pierce -= 1
            if self.pierce == 0:
                self.kill()
                break

