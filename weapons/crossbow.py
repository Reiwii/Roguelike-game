import math
from .Base import BaseWeapon, WeaponLevelStats

class MagicWandWeapon(BaseWeapon):
    id = "magic_wand"
    name = "Magic Blue Wand"

    def __init__(self, level_stats: list[WeaponLevelStats]):
        super().__init__(level_stats)

    def fire(self, world, owner):
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
        length = math.hypot(dx, dy) or 1.0
        vx, vy = dx / length, dy / length

        for _ in range(stats.amount):
            world.spawn_projectile(
                pos=(ox, oy),
                vel=(vx * stats.speed, vy * stats.speed),
                damage=stats.damage,
                pierce=stats.pierce,
                owner=owner,
                radius=0,
                proj="proj"
            )
