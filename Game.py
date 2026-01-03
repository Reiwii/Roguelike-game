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
        self.screen = pygame.display.set_mode((Setting.SCREEN_WIDTH, Setting.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Camera Movement Example")
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

        self.ui = UI.UI(self.screen,self.world)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.ui.handle_event(event)

    def update(self):
        if not self.ui.paused:
            self.world.update(self.dt, self.camera)
        # if self.world.player.leveled_up:
        #     self.world.player.leveled_up = False
        #     self.ui.open_levelup_choices()

    def draw(self):
        self.camera.custom_draw(self.player)
        self.ui.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(59) / 1000

        pygame.quit()

            
if __name__ == "__main__":
    game = Game()
    game.run()