import pygame
from config import THEME_BUTTON, WHITE, THEME_PURPLE, THEME_PURPLE_DARK

class UIManager:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 200)
        self.button_font = pygame.font.Font(None, 50)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.alert_font = pygame.font.Font(None, 48)

    # dessine un bouton avec un effet de profondeur
    def draw_button(self, screen, rect, text, active=False):
        shadow = pygame.Rect(rect.x + 4, rect.y + 4, rect.w, rect.h)
        pygame.draw.rect(screen, (40, 20, 10), shadow)

        color = THEME_BUTTON if not active else (255, 80, 255)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 3)

        t = self.button_font.render(text, True, WHITE)
        t_rect = t.get_rect(center=rect.center)
        screen.blit(t, t_rect)

    # dessine un bouton plus petit pour les options
    def draw_small_button(self, screen, rect, text, active=False):
        shadow = pygame.Rect(rect.x + 3, rect.y + 3, rect.w, rect.h)
        pygame.draw.rect(screen, (40, 20, 10), shadow)

        color = (140, 0, 190) if not active else (255, 80, 255)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)

        t = self.font.render(text, True, WHITE)
        t_rect = t.get_rect(center=rect.center)
        screen.blit(t, t_rect)

    # dessine une alerte au centre de l'écran
    def key_name(self, k):
        try:
            return pygame.key.name(k).upper()
        except:
            return str(k)

    # dessine un titre avec une ombre pour un effet de profondeur
    def draw_title_with_shadow(self, screen, text, center_x, center_y):
        shadow = self.title_font.render(text, True, THEME_PURPLE_DARK)
        shadow_rect = shadow.get_rect(center=(center_x + 6, center_y + 6))
        screen.blit(shadow, shadow_rect)

        title = self.title_font.render(text, True, THEME_PURPLE)
        title_rect = title.get_rect(center=(center_x, center_y))
        screen.blit(title, title_rect)
