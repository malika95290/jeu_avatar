import pygame
from Projectile import Projectile

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()

        # référence au jeu principal
        self.game = game

        # vie du joueur
        self.health = 100
        self.max_health = 100

        # dégâts et vitesse
        self.attack = 10
        self.velocity = 5

        # images du joueur quand il regarde à droite
        self.frames = [
            pygame.image.load("assets/player000.png").convert_alpha(),
            pygame.image.load("assets/player001.png").convert_alpha(),
            pygame.image.load("assets/player002.png").convert_alpha(),
            pygame.image.load("assets/player003.png").convert_alpha(),
            pygame.image.load("assets/player005.png").convert_alpha(),
        ]

        # images du joueur quand il regarde à gauche
        self.frames_left = [
            pygame.image.load("assets/player000-left.png").convert_alpha(),
            pygame.image.load("assets/player001-left.png").convert_alpha(),
            pygame.image.load("assets/player002-left.png").convert_alpha(),
            pygame.image.load("assets/player003-left.png").convert_alpha(),
            pygame.image.load("assets/player005-left.png").convert_alpha(),
        ]

        # on redimensionne toutes les images
        self.frames = [pygame.transform.scale(img, (150, 150)) for img in self.frames]
        self.frames_left = [pygame.transform.scale(img, (150, 150)) for img in self.frames_left]

        # animation
        self.anim_index = 0.0
        self.anim_speed = 0.15

        # image affichée au début
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 520

        # groupe qui contient toutes les boules de feu
        self.all_projectiles = pygame.sprite.Group()

        # variables pour le saut et la gravité
        self.vy = 0
        self.gravity = 1
        self.jump_strength = 18
        self.on_ground = True
        self.ground_y = self.rect.y  

        # direction du joueur
        self.direction = "right"

        # --- tir ---
        self.last_shot_time = 0      # moment où le joueur a tiré la dernière fois
        self.shoot_cooldown = 400    # temps minimum entre deux tirs (en millisecondes)


    def damage(self, amount):
        # enlève de la vie au joueur
        self.health -= amount

        # empêche la vie d'être négative
        if self.health < 0:
            self.health = 0
    

    def update_health_bar(self, surface):
        # couleurs de la barre de vie
        bar_color = (111, 210, 46)
        back_bar_color = (60, 63, 60)

        # largeur maximale de la barre
        max_bar_width = 100

        # largeur actuelle selon la vie
        bar_width = int((self.health / self.max_health) * max_bar_width)

        # position des barres
        bar_position = [self.rect.x + 50, self.rect.y - 20, bar_width, 8]
        back_bar_position = [self.rect.x + 50, self.rect.y - 20, max_bar_width, 8]

        # dessin de la barre de fond
        pygame.draw.rect(surface, back_bar_color, back_bar_position)

        # dessin de la barre de vie
        pygame.draw.rect(surface, bar_color, bar_position)


    def launch_projectile(self):
        # temps actuel du jeu
        current_time = pygame.time.get_ticks()

        # on vérifie si le joueur peut tirer
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            projectile = Projectile(self)
            self.all_projectiles.add(projectile)

            # on enregistre le moment du tir
            self.last_shot_time = current_time


    def move_right(self):
        # le joueur regarde à droite
        self.direction = "right"

        # déplacement si pas de collision
        if not self.game.check_collision(self, self.game.all_ennemies):
            self.rect.x += self.velocity

        # animation
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.frames):
            self.anim_index = 0

        self.image = self.frames[int(self.anim_index)]
    

    def move_left(self):
        # le joueur regarde à gauche
        self.direction = "left"

        # déplacement
        self.rect.x -= self.velocity

        # animation
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.frames_left):
            self.anim_index = 0

        self.image = self.frames_left[int(self.anim_index)]


    def move_air_right(self):
        # déplacement vers la droite en l'air
        self.rect.x += self.velocity  


    def move_air_left(self):
        # déplacement vers la gauche en l'air
        self.rect.x -= self.velocity  


    def jump(self):
        # le joueur peut sauter seulement s'il est au sol
        if self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False


    def apply_gravity(self):
        # appliquer la gravité
        self.vy += self.gravity
        self.rect.y += self.vy

        # collision avec le sol
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vy = 0
            self.on_ground = True
