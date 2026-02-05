import pygame

# Dimensions écran
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

# Niveaux
MAX_LEVEL = 4
FIRE_LEVEL = 3

# Couleurs du thème
THEME_BG = (15, 10, 35)              
THEME_PURPLE = (148, 0, 211)         
THEME_PURPLE_DARK = (75, 0, 130)     
THEME_BUTTON = (191, 0, 255)         

WHITE = (255, 255, 255)

# Tempête de comètes
COMET_EVENT_DURATION = 600  

# Paramètres par défaut
DEFAULT_SETTINGS = {
    "shoot_mode": "mouse",      
    "move_mode": "qd",           
    "pause_key": pygame.K_p,     
    "music_volume": 0.5,         
}
