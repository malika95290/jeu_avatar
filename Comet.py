import pygame
import random

class Comet(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.velocity = 3  # Vitesse de chute
        self.image = pygame.image.load("assets/comete.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        # Position aléatoire X en haut de l'écran
        self.rect.x = random.randint(0, 1000)
        self.rect.y = -50
        self.has_hit = False  # Flag pour éviter les dégâts répétés
    
    def move(self):
        # Descendre la comète
        self.rect.y += self.velocity
        
        # Vérifier collision avec le joueur (une seule fois)
        if self.game.check_collision(self, self.game.all_players) and not self.has_hit:
            self.game.player.damage(10)  # Dégâts fixes de 10
            self.has_hit = True
            self.remove()
        
        # Supprimer si elle dépasse l'écran
        if self.rect.y > 700:
            self.remove()
