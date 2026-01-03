import json
from .Base import WeaponLevelStats
from .MagicWand import MagicWandWeapon
from .Sword import Sword
from .crossbow import CrossbowWeapon
from .Shuriken import Shuriken


WEAPON_CLASSES = {
    "magic_wand": MagicWandWeapon,
    "sword":Sword,
    "crossbow":CrossbowWeapon,
    "shuriken":Shuriken
}

def load_weapon_db(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_levels(level_list):
    return [WeaponLevelStats(**d) for d in level_list]

def create_weapon(weapon_id: str, db: dict):
    cfg = db[weapon_id]
    levels = build_levels(cfg["levels"])
    cls = WEAPON_CLASSES[weapon_id]
    return cls(levels)
