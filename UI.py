import pygame

class UI:
    def __init__(self, screen,world):
        self.screen = screen
        self.paused = False
        self.world = world

        self.X_button = pygame.image.load("assets/X.png").convert_alpha()
        pause_button = pygame.image.load("assets/Pause.png").convert_alpha()
        self.pause_button = pygame.transform.scale_by(pause_button,3)
        resume_button = pygame.image.load("assets/resume.png").convert_alpha()
        self.resume_button = pygame.transform.scale_by(resume_button,3)
        self.weapon_holder = pygame.image.load("assets/MediavelFree.png").convert_alpha()
        self.health_bar = HealthBar(20,20,150,20,100,world)

        self.pause_rect = self.pause_button.get_rect(topright=(screen.get_width() - 20, 20))
        self.resume_rect = self.resume_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        self.weapon_rect = self.weapon_holder.get_rect(bottomleft=(20, screen.get_height() - 20))

        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  

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
        self.screen.blit(self.weapon_holder, self.weapon_rect)
        self.health_bar.draw(self.screen,self.world)

        if self.paused:
            self.screen.blit(self.overlay, (0, 0))
            self.screen.blit(self.resume_button, self.resume_rect)

class HealthBar():
    def __init__(self, x, y, w, h, max_hp,world):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = world.player.hp
        self.max_hp = max_hp

    def draw(self, surface,world):
        self.hp = world.player.hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
    