import pygame
from Projectile import Projectile

# Définir une classe Player avec des attributs de base
class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.frames = [
            pygame.image.load("assets/player000.png").convert_alpha(),
            pygame.image.load("assets/player001.png").convert_alpha(),
            pygame.image.load("assets/player002.png").convert_alpha(),
            pygame.image.load("assets/player003.png").convert_alpha(),
            pygame.image.load("assets/player005.png").convert_alpha(),
        ]
        self.frames_left = [
            pygame.image.load("assets/player000-left.png").convert_alpha(),
            pygame.image.load("assets/player001-left.png").convert_alpha(),
            pygame.image.load("assets/player002-left.png").convert_alpha(),
            pygame.image.load("assets/player003-left.png").convert_alpha(),
            pygame.image.load("assets/player005-left.png").convert_alpha(),
        ]
        self.frames = [pygame.transform.scale(img, (150, 150)) for img in self.frames]
        self.frames_left = [pygame.transform.scale(img, (150, 150)) for img in self.frames_left]

        self.anim_index = 0.0
        self.anim_speed = 0.15
        # Image initiale
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 520

        self.all_projectiles = pygame.sprite.Group()

        self.vy = 0
        self.gravity = 1
        self.jump_strength = 18
        self.on_ground = True
        self.ground_y = self.rect.y  

        self.direction = "right"

    def damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def update_health_bar(self, surface):
        # Définir la couleur de la barre de vie
        bar_color = (111, 210, 46)
        back_bar_color = (60, 63, 60)
        # Taille maximale souhaitée de la barre (en pixels)
        max_bar_width = 100
        # Calculer la largeur proportionnelle selon la santé
        bar_width = int((self.health / self.max_health) * max_bar_width)
        # Définir la position et la taille de la barre de vie
        bar_position = [self.rect.x + 50, self.rect.y - 20, bar_width, 8]
        back_bar_position = [self.rect.x + 50, self.rect.y - 20, max_bar_width, 8]
        # Dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def launch_projectile(self):
        projectile = Projectile(self)
        self.all_projectiles.add(projectile)

    

    def move_right(self):
        self.direction = "right"
        if not self.game.check_collision(self, self.game.all_ennemies):
            self.rect.x += self.velocity
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]
    
    def move_left(self):
        self.direction = "left"
        self.rect.x -= self.velocity
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.frames_left):
            self.anim_index = 0
        self.image = self.frames_left[int(self.anim_index)]

    def move_air_right(self):
        self.rect.x += self.velocity  

    def move_air_left(self):
        self.rect.x -= self.velocity  


    def jump(self):
        if self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        self.vy += self.gravity
        self.rect.y += self.vy

        # sol
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vy = 0
            self.on_ground = True
