import pygame
from Player import Player
from Enemy import Enemy
from Comet import Comet
import os
import cv2

class Game:
    def __init__(self):
        self.level_number = 1
        self.player = Player(self)
        self.all_players = pygame.sprite.Group()
        self.all_players.add(self.player)
        self.pressed = {}
        self.all_ennemies = pygame.sprite.Group()
        self.all_comets = pygame.sprite.Group()
        self.comet_spawn_timer = 0
        self.enemies_killed = 0
        self.wave_size = 5

        # première vague
        self.spawn_wave(self.wave_size)
        # Charger la vidéo
        video_path = os.path.join(os.path.dirname(__file__), "assets/Dragon_incrusté_dans_les_montagnes.mp4")
        self.menu_video = cv2.VideoCapture(video_path)
    
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def display_monster(self):
        """Ajoute UN ennemi"""
        ennemie = Enemy(self)
        self.all_ennemies.add(ennemie)
    
    def spawn_wave(self, n=5):
        """Crée une vague de n ennemis (une seule fois)"""
        self.all_ennemies.empty()
        i = 0
        for i in range(n):
            self.display_monster()
            i += 1

