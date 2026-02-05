import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        """Initialise un projectile avec sa vitesse, son image, et sa position de départ en fonction du joueur"""
        super().__init__()
        self.velocity = 3
        self.player = player
        self.image = pygame.image.load("assets/projectile_fire.png")
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.hit_sound = pygame.mixer.Sound("assets/fire.mp3")
        self.hit_sound.set_volume(0.1)
        self.rect = self.image.get_rect()
        self.rect.y = player.rect.y + 10
        if player.direction == "right":
            self.velocity = 8
            self.rect.x = player.rect.x + 100
        else:
            self.velocity = -8
            self.rect.x = player.rect.x - 50

    def move(self):
        """Déplace le projectile, vérifie les collisions avec les ennemis, et le supprime s'il dépasse l'écran"""
        self.rect.x += self.velocity
        for enemy in self.player.game.check_collision(self, self.player.game.all_ennemies):
            if self in self.player.all_projectiles:
                self.player.all_projectiles.remove(self)
            self.remove()
            enemy.damage(self.player.attack)
            self.hit_sound.play(maxtime=600)

            return
        if self.rect.x > 1366:
            if self in self.player.all_projectiles:
                self.player.all_projectiles.remove(self)

        