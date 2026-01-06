import math
from .Base import BaseWeapon, WeaponLevelStats

class Shuriken(BaseWeapon):
    id = "shuriken"
    name = "Shuriken"

    def __init__(self, level_stats: list[WeaponLevelStats]):
        super().__init__(level_stats)

    def fire(self, world, owner)->None:
        stats = self.final_stats(owner.combat_stats)

        target = None
        best_d2 = None
        ox, oy = owner.rect.center
        for e in world.enemies_group:
            if e.action == "die":
                continue
            ex, ey = e.rect.center
            d2 = (ex - ox) ** 2 + (ey - oy) ** 2
            if best_d2 is None or d2 < best_d2:
                best_d2 = d2
                target = e

        if target is None:
            return

        tx, ty = target.rect.center
        dx, dy = tx - ox, ty - oy
        length = math.hypot(dx, dy) 
        if length == 0:
            length = 1
        vx, vy = dx / length, dy / length

        base_vx,base_vy = vx * stats.speed, vy * stats.speed
        spread = 50
        for i in range(stats.amount):
            offset = i * spread
            world.spawn_projectile(
                pos=(ox, oy),
                vel=(base_vx + offset,base_vy - offset),
                damage=stats.damage,
                pierce=stats.pierce,
                owner=owner,
                projectile_id ="shuriken",
            )
