import json
from .Base import WeaponLevelStats
from .MagicWand import MagicWandWeapon

WEAPON_CLASSES = {
    "magic_wand": MagicWandWeapon,
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
