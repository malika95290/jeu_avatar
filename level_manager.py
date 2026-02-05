import pygame

class LevelManager:
    def __init__(self, game, screen, settings_manager):
        self.game = game
        self.screen = screen
        self.settings = settings_manager
        self.background = None
        self.bg_x = 0

    def load_level(self, level_number: int):
        """Charge le background et les paramètres du niveau spécifié, et ajuste la position des ennemis en conséquence"""
        self.bg_x = 0
        if level_number == 1:
            self.background = pygame.image.load("assets/background_jungle.png").convert()
            self.game.player.ground_y = 520
            self.settings.play_music("assets/avatar_sound.mp3")
        elif level_number == 2:
            self.background = pygame.image.load("assets/background_ocean.jpg").convert()
            self.game.player.ground_y = 520
        elif level_number == 3:
            self.background = pygame.image.load("assets/background_fire.jpg").convert()
            self.game.player.ground_y = 490
        elif level_number == 4:
            self.background = pygame.image.load("assets/background_sky.jpg").convert()
            self.game.player.ground_y = 480
        else:
            return
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        for e in self.game.all_ennemies:
            e.rect.bottom = self.game.player.ground_y

    def draw_scrolling_background(self, bg_speed):
        """Fait défiler le background horizontalement pour créer un effet de mouvement continu"""
        self.bg_x -= bg_speed
        if self.bg_x <= -self.background.get_width():
            self.bg_x = 0
        elif self.bg_x >= self.background.get_width():
            self.bg_x = 0
        # dessine 2 backgrounds pour l'effet "infini"
        self.screen.blit(self.background, (self.bg_x, 0))
        self.screen.blit(self.background, (self.bg_x + self.background.get_width(), 0))
