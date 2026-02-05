import pygame
import random

class Comet(pygame.sprite.Sprite):
    def __init__(self, game):
        """Initialise une comète avec sa vitesse, son image, et sa position de départ"""
        super().__init__()
        self.game = game
        self.velocity = 3  
        self.image = pygame.image.load("assets/comete.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1000)
        self.rect.y = -50
        self.has_hit = False 
    
    def move(self):
        """Déplace la comète vers le bas, vérifie les collisions avec le joueur, et la supprime si elle dépasse l'écran"""
        self.rect.y += self.velocity
        if self.game.check_collision(self, self.game.all_players) and not self.has_hit:
            self.game.player.damage(10)  # Dégâts fixes de 10
            self.has_hit = True
            self.remove()
        if self.rect.y > 700:
            self.remove()
