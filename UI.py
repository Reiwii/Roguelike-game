import pygame

class UI:
    def __init__(self, screen, world):
        self.screen = screen
        self.paused = False
        self.world = world
        self.weapon_rows = 2
        self.weapon_cols = 4
        self.slot_size = 48   
        self.slot_gap = 8    

        self.X_button = pygame.image.load("assets/X.png").convert_alpha()
        pause_button = pygame.image.load("assets/Pause.png").convert_alpha()
        self.pause_button = pygame.transform.scale_by(pause_button, 3)

        resume_button = pygame.image.load("assets/resume.png").convert_alpha()
        self.resume_button = pygame.transform.scale_by(resume_button, 3)


        self.weapon_icons = {
            "magic_wand": self.world.assets["magic_wand"],
            "sword": self.world.assets["sword"],
            "crossbow": self.world.assets["crossbow"]
        }

        self.attribute_icons = {
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if not self.paused:
                if self.pause_rect.collidepoint(mouse_pos):
                    self.paused = True
            else:
                if self.resume_rect.collidepoint(mouse_pos):
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


        for i, a in enumerate(self.world.player.attributes):
            icon = self.attr_icons.get(a.id)
            if icon:
                self.screen.blit(icon, icon.get_rect(center=slots[4 + i].center))



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
