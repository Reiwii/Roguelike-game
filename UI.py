import pygame
from weapons.weapons_from_json import create_weapon
from Player import Attribute

class UI:
    def __init__(self, screen, world):
        self.screen = screen
        self.paused = False
        self.world = world
        self.weapon_rows = 2
        self.weapon_cols = 3
        self.slot_size = 48   
        self.slot_gap = 8    
        self.mouse_pos = (0,0)

        self.X_button = pygame.image.load("assets/X.png").convert_alpha()
        pause_button = pygame.image.load("assets/Pause.png").convert_alpha()
        self.pause_button = pygame.transform.scale_by(pause_button, 3)

        resume_button = pygame.image.load("assets/resume.png").convert_alpha()
        self.resume_button = pygame.transform.scale_by(resume_button, 3)


        self.weapon_icons = {
            "magic_wand": self.world.assets["magic_wand"],
            "sword": self.world.assets["sword"],
            "crossbow": self.world.assets["crossbow"],
            "shuriken": self.world.assets["shuriken"],
        }
        self.attribute_icons = {
            "elixir": self.world.assets["elixir"],
            "hook": self.world.assets["hook"],
            "kubek_deluxe": self.world.assets["kubek_deluxe"],
            "lamp": self.world.assets["lamp"],
            "ring": self.world.assets["ring"],
            "scroll": self.world.assets["scroll"],
        }


        self.health_bar = HealthBar(
            20, 20, 180, 22,
            self.world.player.max_hp,
            self.world.player.hp
        )

        self.exp_bar = ExpBar(
            20, 60, 180, 22,
            self.world.player.xp_to_next_level,
            self.world.player.xp
        )

        self.pause_rect = self.pause_button.get_rect(
            topright=(screen.get_width() - 20, 20)
        )

        self.resume_rect = self.resume_button.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )

        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        self.font = pygame.font.Font(None, 20)
        self.upgrade_open = False
        self.offers = []          
        self.offer_rects = []    

        self.upgrade_font = pygame.font.Font(None, 28)
        self.upgrade_small = pygame.font.Font(None, 20)


    def on_resize(self, screen):
        self.screen = screen

        self.pause_rect = self.pause_button.get_rect(
            topright=(screen.get_width() - 20, 20)
        )
        self.resume_rect = self.resume_button.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )

        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        if self.upgrade_open:
            self._build_offer_rects()
    def apply_offer(self, offer):
        p = self.world.player

        if offer.kind == "weapon":
            for w in p.weapons:
                if w.id == offer.id:
                    w.level_up()
                    return

            # not owned yet
            new_w = create_weapon(offer.id, self.world.weapon_db)
            p.weapons.append(new_w)
            return

        # attribute
        attr = p.attributes.get(offer.id)
        if attr is None:
            p.attributes[offer.id] = Attribute(id=offer.id, level=1, max_level=5)
        else:
            attr.level_up()

        p.recalculate_combat_stats()


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_pos = event.pos

            if not self.paused:
                if self.pause_rect.collidepoint(self.mouse_pos):
                    self.paused = True
            else:
                if self.resume_rect.collidepoint(self.mouse_pos):
                    self.paused = False
        if self.upgrade_open and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.offer_rects):
                if r.collidepoint(event.pos):
                    self.apply_offer(self.offers[i])
                    self.upgrade_open = False
                    self.paused = False

    def draw(self):
        self.screen.blit(self.pause_button, self.pause_rect)

        slots = self.get_weapon_slot_rects()
        for slot in slots:
            pygame.draw.rect(self.screen, (40, 40, 40), slot)          
            pygame.draw.rect(self.screen, (200, 200, 200), slot, 2)
        self.draw_player_loadout(slots)

        self.health_bar.update(self.world)
        self.exp_bar.update(self.world)

        self.health_bar.draw(self.screen)
        self.exp_bar.draw(self.screen)

        if self.paused:
            self.screen.blit(self.overlay, (0, 0))
            self.screen.blit(self.resume_button, self.resume_rect)
        if self.upgrade_open:
            self.draw_upgrade_menu()


    def get_weapon_slot_rects(self):
        start_x = 20
        start_y = self.screen.get_height() - 120  

        rects = []
        for r in range(self.weapon_rows):
            for c in range(self.weapon_cols):
                x = start_x + c * (self.slot_size + self.slot_gap)
                y = start_y + r * (self.slot_size + self.slot_gap)
                rects.append(pygame.Rect(x, y, self.slot_size, self.slot_size))
        return rects

    def draw_player_loadout(self,slots):
        for r in slots:
            pygame.draw.rect(self.screen, (40, 40, 40), r)
            pygame.draw.rect(self.screen, (200, 200, 200), r, 2)

        for i, w in enumerate(self.world.player.weapons):
            if i >= self.weapon_cols:
                break
            icon = self.weapon_icons.get(w.id)
            if icon:
                self.screen.blit(icon, icon.get_rect(center=slots[i].center))
            cur = w.level
            mx  = w.max_level
            lvl_surf = self.font.render(f"({cur}/{mx})", True, (255, 255, 255))

            pad = 2
            bg = lvl_surf.get_rect(bottomright=(slots[i].right - 4, slots[i].bottom - 2)).inflate(pad*2, pad*2)
            pygame.draw.rect(self.screen, (0, 0, 0), bg, border_radius=4)

            self.screen.blit(lvl_surf, lvl_surf.get_rect(bottomright=(slots[i].right - 4, slots[i].bottom - 2)))

        for i, a in enumerate(self.world.player.attributes.values()):
            if i >= self.weapon_cols:  
                break
            icon = self.attribute_icons.get(a.id)
            if icon:
                slot_index = self.weapon_cols + i   
                self.screen.blit(icon, icon.get_rect(center=slots[slot_index].center))
            cur = a.level
            mx  = a.max_level
            lvl_surf = self.font.render(f"({cur}/{mx})", True, (255, 255, 255))

            pad = 2
            bg = lvl_surf.get_rect(bottomright=(slots[slot_index].right - 4, slots[slot_index].bottom - 2)).inflate(pad*2, pad*2)
            pygame.draw.rect(self.screen, (0, 0, 0), bg, border_radius=4)
            self.screen.blit(lvl_surf, lvl_surf.get_rect(bottomright=(slots[slot_index].right - 4, slots[slot_index].bottom - 2)))


    def open_upgrade(self, offers):
        self.paused = True
        self.upgrade_open = True
        self.offers = offers[:]          
        self._build_offer_rects()

    def _build_offer_rects(self):
        sw, sh = self.screen.get_size()
        card_w, card_h = 220, 110
        gap = 18

        total_w = card_w * 3 + gap * 2
        start_x = (sw - total_w) // 2
        y = sh // 2 - card_h // 2

        self.offer_rects = [
            pygame.Rect(start_x + i * (card_w + gap), y, card_w, card_h)
            for i in range(3)
        ]

    def draw_upgrade_menu(self):
        if not self.upgrade_open:
            return

        self.screen.blit(self.overlay, (0, 0))

        sw, sh = self.screen.get_size()

        title = self.upgrade_font.render("Choose an upgrade", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(sw // 2, sh // 2 - 110)))

        mouse_pos = self.mouse_pos

        for i, rect in enumerate(self.offer_rects):
            if i >= len(self.offers):
                continue
            offer = self.offers[i]

            hovered = rect.collidepoint(mouse_pos)

            bg_col = (55, 55, 65) if not hovered else (75, 75, 95)
            border_col = (210, 210, 210) if not hovered else (255, 255, 255)

            pygame.draw.rect(self.screen, bg_col, rect, border_radius=10)
            pygame.draw.rect(self.screen, border_col, rect, width=3, border_radius=10)

            if offer.kind == "weapon":
                icon = self.weapon_icons.get(offer.id)
            else:
                icon = self.attribute_icons.get(offer.id)

            icon_center = (rect.left + 40, rect.centery)
            if icon:
                self.screen.blit(icon, icon.get_rect(center=icon_center))
            name_x = rect.left + 80
            name_y = rect.top + 18

            name_surf = self.upgrade_small.render(offer.title, True, (255, 255, 255))
            self.screen.blit(name_surf, (name_x, name_y))

            cur, mx = self._get_offer_levels(offer)
            lvl_surf = self.upgrade_small.render(f"({cur}/{mx})", True, (220, 220, 220))
            self.screen.blit(lvl_surf, (name_x, name_y + 28))

            hint = self.upgrade_small.render("Click to pick", True, (180, 180, 180))
            self.screen.blit(hint, (name_x, name_y + 56))

    def _get_offer_levels(self, offer):
        p = self.world.player

        if offer.kind == "weapon":
            for w in p.weapons:
                if w.id == offer.id:
                    return (w.level, w.max_level)
            return (0, 5)

        attr = p.attributes.get(offer.id)
        if attr:
            return (attr.level, attr.max_level)
        return (0, 5)




class Bar:
    def __init__(self, x, y, w, h, max_val, val):
        self.rect = pygame.Rect(x, y, w, h)
        self.val = val
        self.max_val = max_val
        self.font = pygame.font.Font(None, 18)

    def draw(self, surface):
        ratio = max(0, min(1, self.val / self.max_val))

        pygame.draw.rect(surface, (60, 60, 60), self.rect)

        fill_rect = self.rect.copy()
        fill_rect.width = int(self.rect.width * ratio)
        pygame.draw.rect(surface, (0, 200, 0), fill_rect)

        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

    def update(self, world):
        pass


class HealthBar(Bar):
    def update(self, world):
        self.val = world.player.hp
        self.max_val = world.player.max_hp

    def draw(self, surface):
        super().draw(surface)

        text = self.font.render(
            f"HP: {self.val}/{self.max_val}",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)


class ExpBar(Bar):
    def __init__(self, x, y, w, h, max_val, val):
        super().__init__(x, y, w, h, max_val, val)
        self.level = 1
    def update(self, world):
        self.val = world.player.xp
        self.max_val = world.player.xp_to_next_level
        self.level = world.player.level

    def draw(self, surface):
        super().draw(surface)

        text = self.font.render(
            f"LVL {self.level}",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

from dataclasses import dataclass
import random

@dataclass
class Offer:
    kind: str          
    id: str            
    title: str         

def build_offers(world) -> list[Offer]:
    p = world.player
    offers: list[Offer] = []

    MAX_WEAPONS = 3
    MAX_ATTRS   = 3

    weapons_full = len(p.weapons) >= MAX_WEAPONS
    attrs_full   = len(p.attributes) >= MAX_ATTRS  

    owned_weapon_ids = {w.id for w in p.weapons}
    for wid in world.all_weapon_ids:
        if wid in owned_weapon_ids:
            w = next(w for w in p.weapons if w.id == wid)
            if w.can_level_up():
                offers.append(Offer("weapon", wid, f"{wid} +1"))
        else:
            if not weapons_full:
                offers.append(Offer("weapon", wid, f"Get {wid}"))

    all_attr_ids = ["elixir", "hook", "kubek_deluxe","lamp",  "ring", "scroll"]
    for aid in all_attr_ids:
        if aid in p.attributes:
            if p.attributes[aid].can_level_up():
                offers.append(Offer("attr", aid, f"{aid} +1"))
        else:
            if not attrs_full:
                offers.append(Offer("attr", aid, f"Get {aid}"))

    return offers


def roll_3_offers(world) -> list[Offer]:
    pool = build_offers(world)
    if not pool:
        return []
    return random.sample(pool, k=min(3, len(pool)))