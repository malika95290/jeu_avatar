import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 50
        self.max_health = 50
        self.attack = 5
        self.velocity = 1
        
        self.frames = [
            pygame.image.load("assets/dragon1.png").convert_alpha(),
            pygame.image.load("assets/dragon2.png").convert_alpha(),
            pygame.image.load("assets/dragon3.png").convert_alpha(),
            pygame.image.load("assets/dragon4.png").convert_alpha(),
            pygame.image.load("assets/dragon5.png").convert_alpha(),
            pygame.image.load("assets/dragon6.png").convert_alpha(),
        ]
        self.frames = [pygame.transform.scale(img, (150, 150)) for img in self.frames]

        self.anim_index = 0.0
        self.anim_speed = 0.15

        # Image initiale
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 700 + random.randint(0, 500)  
        self.rect.bottom = self.game.player.ground_y + 110
        
        self.x = float(self.rect.x)  # Accumulateur de position

    def damage(self, amount):
        self.health -= amount
        # NE PAS réinitialiser la santé - laisser l'ennemi mourir
        # La gestion de la mort se fait dans la boucle principale

    def update_health_bar(self, surface):
        bar_color = (111, 210, 46)
        back_bar_color = (60, 63, 60)
        max_bar_width = 50
        # Calculer la largeur proportionnelle selon la santé
        bar_width = int((self.health / self.max_health) * max_bar_width)
        # Définir la position et la taille de la barre de vie
        bar_position = [self.rect.x + 50, self.rect.y - 20, bar_width, 8]
        back_bar_position = [self.rect.x + 50, self.rect.y - 20, max_bar_width, 8]
        # Dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def animate(self):
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]

    def move(self):
        # S'il n'y a pas collision avec le joueur
        if not self.game.check_collision(self, self.game.all_players):

            # Déplacement
            self.rect.x -= self.velocity

            # Bord gauche → repartir à droite
            if self.rect.x <= 0:
                self.rect.x = 0
                self.velocity = 2

            # Bord droit → repartir à gauche
            elif self.rect.x + self.rect.width >= 1366:
                self.rect.x = 1366 - self.rect.width
                self.velocity = -2

        # Collision avec le joueur
        else:
            self.game.player.damage(0.5)
