from .Base import BaseWeapon, WeaponLevelStats

class Sword(BaseWeapon):
    id = "sword"
    name = "Sword"

    def __init__(self, level_stats):
        super().__init__(level_stats)

    def fire(self, world, owner):
        stats = self.final_stats(owner.combat_stats)
        ox, oy = owner.rect.center

        for _ in range(stats.amount):
            world.spawn_projectile(
                pos=(ox, oy),
                vel=0,
                damage=stats.damage,
                pierce=stats.pierce,
                owner=owner,
                projectile_id="slash",
            )
