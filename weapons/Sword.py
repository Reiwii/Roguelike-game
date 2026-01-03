from .Base import BaseWeapon, WeaponLevelStats

class Sword(BaseWeapon):
    id = "sword"
    name = "Sword"

    def __init__(self, level_stats, evolution = None):
        super().__init__(level_stats, evolution)

    def fire(self, world, owner):
        stats = self.final_stats(owner.combat_stats)
        ox, oy = owner.rect.center

        base_radius = 100
        radius = base_radius * max(0.25, stats.area if stats.area != 0 else 1.0)

        for _ in range(stats.amount):
            world.spawn_projectile(
                pos=(ox, oy),
                vel=0,
                damage=stats.damage,
                radius=radius,
                pierce=stats.pierce,
                owner=owner,
                projectile_id="slash"
            )
