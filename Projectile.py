import pygame

class DamageHitbox(pygame.sprite.Sprite):
    def __init__(self, pos, damage, pierce, owner, radius, image, *groups):
        super().__init__(*groups)
        self.owner = owner
        self.pos = pygame.Vector2(pos)

        self.damage = damage
        self.pierce = pierce          #-1 inf
        self.radius = radius          
        self.enemies_hit = set()

        self.image = image
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

    def on_hit_enemy(self, world, enemy):
        enemy.take_damage(self.damage, world, world.player.pos)

    def handle_hits(self, world):
        hits = pygame.sprite.spritecollide(self, world.enemies_group, False, collided=pygame.sprite.collide_circle)
        for e in hits:
            if e.action  == "die":
                continue
            if e in self.enemies_hit:
                continue

            self.enemies_hit.add(e)
            self.on_hit_enemy(world, e)

            if self.pierce == -1:
                continue
            self.pierce -= 1
            if self.pierce <= 0:
                self.kill()
                break


class LinearProjectile(DamageHitbox):
    def __init__(self, pos, vel, damage, pierce, owner, image, radius=3, *groups):
        self.vel = pygame.Vector2(vel)
        super().__init__(pos, damage, pierce, owner, radius, image, *groups)

    def update(self, world, dt):
        if not world.despawn_rect.colliderect(self.rect):
            self.kill()
            return

        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.handle_hits(world)


class FollowOwnerHitbox(DamageHitbox):
    def __init__(self, owner, damage, pierce, radius, image, lifetime, *groups):
        super().__init__(owner.rect.center, damage, pierce, owner, radius, image, *groups)
        self.lifetime = lifetime

    def update(self, world, dt):
        self.pos.update(self.owner.rect.center)
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        self.handle_hits(world)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
