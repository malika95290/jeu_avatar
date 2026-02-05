import pygame
from config import DEFAULT_SETTINGS

class SettingsManager:

    # initialise les paramètres du jeu
    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()

    # retourne les touches pour aller à gauche et à droite
    def get_move_keys(self):
        if self.settings["move_mode"] == "arrows":
            return pygame.K_LEFT, pygame.K_RIGHT
        return pygame.K_q, pygame.K_d

    # change le volume de la musique
    def set_music_volume(self, v):
        v = max(0.0, min(1.0, v))
        self.settings["music_volume"] = v
        pygame.mixer.music.set_volume(self.settings["music_volume"])

    # lance une musique en boucle
    def play_music(self, path):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        self.set_music_volume(self.settings["music_volume"])
