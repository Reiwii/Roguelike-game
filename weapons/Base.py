from dataclasses import dataclass



@dataclass(slots=True)
class WeaponLevelStats:
    damage: int
    cooldown: float                 
    amount: int = 1
    speed: float = 0.0              
    duration: float = 0.0           
    area: float = 0.0               
    pierce: int = 0                 


@dataclass(slots=True)
class EvolutionRule:
    required_passive_id: str
    evolved_weapon_id: str


class BaseWeapon:
    id: str = "base"
    name: str = "Base Weapon"
    def __init__(self,level_stats: list[WeaponLevelStats],evolution: list[EvolutionRule] | None = None,):
        self._levels = level_stats
        self.level = 1
        self.max_level = len(level_stats)
        self._cooldown_timer = 0.0
        self.evolution = evolution

    def can_level_up(self) -> bool:
        return self.level < self.max_level

    def level_up(self) -> None:
        if self.can_level_up():
            self.level += 1

    def base_stats(self) -> WeaponLevelStats:
        return self._levels[self.level - 1]

    def final_stats(self, owner_stats) -> WeaponLevelStats:
        b = self.base_stats()
        return WeaponLevelStats(
            damage=int(b.damage * owner_stats.might_mult),
            cooldown=max(0.05, b.cooldown * owner_stats.cooldown_mult),
            amount=b.amount + owner_stats.amount_bonus,
            speed=b.speed * owner_stats.speed_mult,
            duration=b.duration * owner_stats.duration_mult,
            area=b.area * owner_stats.area_mult,
            pierce=b.pierce + owner_stats.pierce_bonus,
        )

    def update(self, dt: float, world, owner) -> None:
        self._cooldown_timer = max(0.0, self._cooldown_timer - dt)
        if self._cooldown_timer == 0.0:
            self.fire(world, owner)
            self._cooldown_timer = self.final_stats(owner.combat_stats).cooldown

    def fire(self, world, owner) -> None:
        raise NotImplementedError
 