import pygame
import Setting
import Camera
import Player
import World
from weapons.weapons_from_json import load_weapon_db,create_weapon
class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Setting.SCREEN_WIDTH, Setting.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Camera Movement Example")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
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
        weapon_db = load_weapon_db("weapons/weapons.JSON")
        magic_wand = create_weapon("magic_wand", weapon_db)
        self.player.weapons.append(magic_wand)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.world.update(self.dt, self.camera)

    def draw(self):
        self.camera.custom_draw(self.player)
        pygame.display.flip()
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

            
if __name__ == "__main__":
    game = Game()
    game.run()