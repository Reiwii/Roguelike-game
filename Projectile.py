import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, vel, damage, pierce, owner, *groups):
        super().__init__(*groups)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.damage = damage
        self.pierce = pierce
        self.owner = owner

        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, world, dt):
        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        hits = pygame.sprite.spritecollide(self, world.enemies_group, False)
        for e in hits:
            e.take_damage(self.damage)
            self.kill()

