import pygame
import Setting
import Camera
import Player
import World
from weapons.weapons_from_json import load_weapon_db,create_weapon
import UI
class Game():
    def __init__(self):
        pygame.init()
        self.res = (Setting.SCREEN_WIDTH,Setting.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.res, pygame.RESIZABLE)
        self.render_surface = pygame.Surface(self.res)
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = -1
        self.enemies_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()
        self.exp_orb_group = pygame.sprite.Group()
        self.chest_group = pygame.sprite.Group()

        self.camera = Camera.Camera()
        self.player = Player.Player(self.camera,self.all_sprites_group)
        self.world = World.World(self.screen,self.player,self.camera,
                                 self.enemies_group,self.all_sprites_group,
                                 self.projectile_group,self.exp_orb_group,
                                 self.chest_group)
        sword = create_weapon("sword", self.world.weapon_db)
        self.player.weapons.append(sword)

        self.ui = UI.UI(self.render_surface,self.world)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                self.ui.on_resize(self.render_surface)

            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                curr_screen_w, curr_screen_h = self.screen.get_size()
                scale_x = Setting.SCREEN_WIDTH / curr_screen_w
                scale_y = Setting.SCREEN_HEIGHT / curr_screen_h
                scaled_pos = (event.pos[0] * scale_x, event.pos[1] * scale_y)
                event.pos = scaled_pos
            self.ui.handle_event(event)

    def update(self):
        if not self.ui.paused:
            self.world.update(self.dt, self.camera)
        if self.world.player.leveled_up:
            self.world.player.leveled_up = False
            offers = UI.roll_3_offers(self.world)
            if offers:                      
                self.ui.open_upgrade(offers)
            else:
                self.world.player.hp = self.world.player.max_hp

    def draw(self):
        self.render_surface.fill((0,0,0)) 
        self.camera.custom_draw(self.player, self.render_surface)
        self.ui.draw()
        scaled = pygame.transform.scale(self.render_surface, self.screen.get_size())
        self.screen.blit(scaled, (0, 0))

        pygame.display.flip()


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
            print(self.clock.get_fps())

        pygame.quit()

            
if __name__ == "__main__":
    game = Game()
    game.run()