import pygame

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()

        # vitesse de base du projectile
        self.velocity = 3
        self.player = player

        # image de la boule de feu
        self.image = pygame.image.load("assets/projectile_fire.png")
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.y = player.rect.y + 10

        # si le joueur regarde à droite
        if player.direction == "right":
            self.velocity = 8
            self.rect.x = player.rect.x + 100

        # si le joueur regarde à gauche
        else:
            self.velocity = -8
            self.rect.x = player.rect.x - 50

    def move(self):
        self.rect.x += self.velocity
        # Vérifier la collision avec les ennemis
        for enemy in self.player.game.check_collision(self, self.player.game.all_ennemies):
            if self in self.player.all_projectiles:
                self.player.all_projectiles.remove(self)
            self.remove()
            enemy.damage(self.player.attack)
            return

        # Supprimer le projectile s'il dépasse l'écran
        if self.rect.x > 1366:
            if self in self.player.all_projectiles:
                self.player.all_projectiles.remove(self)

        