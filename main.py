import pygame
from Game import Game
from Comet import Comet
import cv2
import numpy as np

# ----------------------------
# INIT PYGAME
# ----------------------------
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("World of Fire")
screen = pygame.display.set_mode((1366, 768))
clock = pygame.time.Clock()

# ----------------------------
# CONSTANTES
# ----------------------------
MAX_LEVEL = 4         # 1 jungle, 2 eau, 3 feu, 4 air/sky
FIRE_LEVEL = 3        # tempête uniquement ici

# ----------------------------
# FONTS
# ----------------------------
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 200)
button_font = pygame.font.Font(None, 50)
subtitle_font = pygame.font.Font(None, 48)
alert_font = pygame.font.Font(None, 48)


# ----------------------------
# UI RECTANGLES
# ----------------------------
play_button = pygame.Rect(560, 500, 250, 80)
panel_rect = pygame.Rect(1100, 0, 240, 100)

# ----------------------------
# GAME OBJECT
# ----------------------------
game = Game()

# ----------------------------
# STATES
# ----------------------------
state = "menu"  # "menu" / "game" / "transition" / "game_over" / "victory"

# ----------------------------
# SCROLLING BACKGROUND
# ----------------------------
bg_x = 0
bg_speed = 0

# ----------------------------
# COMET EVENT (tempête)
# ----------------------------
comet_event_active = False
comet_event_timer = 0
COMET_EVENT_DURATION = 600  # 10 secondes à 60 FPS

def play_music(path):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
# ----------------------------
# LEVEL LOADING
# ordre : Jungle -> Eau -> Feu -> Air
# ----------------------------
def load_level(level_number: int):
    """Charge le décor + règle le sol."""
    global background, bg_x

    bg_x = 0  # reset du scroll quand on change de monde

    if level_number == 1:
        background = pygame.image.load("assets/background_jungle.png").convert()
        game.player.ground_y = 520
        play_music("assets/avatar_sound.mp3")

    elif level_number == 2:
        background = pygame.image.load("assets/background_ocean.jpg").convert()
        game.player.ground_y = 520

    elif level_number == 3:
        background = pygame.image.load("assets/background_fire.jpg").convert()
        game.player.ground_y = 520

    elif level_number == 4:
        background = pygame.image.load("assets/background_sky.jpg").convert()
        game.player.ground_y = 480

    else:
        # Niveau au-delà -> rien à charger ici
        return

    background = pygame.transform.scale(background, screen.get_size())

    # Replacer les ennemis déjà présents (si besoin)
    for e in game.all_ennemies:
        e.rect.bottom = game.player.ground_y


# Charger niveau 1 au démarrage (Jungle)
game.level_number = 1
load_level(game.level_number)


def reset_run():
    """Relance une partie complète depuis le niveau 1."""
    global state, comet_event_active, comet_event_timer, bg_x

    state = "game"
    game.pressed = {}

    # Reset player + groupes
    game.player.health = game.player.max_health
    game.player.rect.x = 100
    game.all_comets.empty()
    game.all_ennemies.empty()

    # Reset tempête
    comet_event_active = False
    comet_event_timer = 0
    game.comet_spawn_timer = 0

    # Niveau 1
    game.level_number = 1
    load_level(game.level_number)

    # Spawn vague
    game.spawn_wave(game.wave_size)

    bg_x = 0


# ----------------------------
# MAIN LOOP
# ----------------------------
running = True
while running:
    # ----------------------------
    # EVENTS
    # ----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "menu" and play_button.collidepoint(event.pos):
                reset_run()

            elif state == "game":
                game.player.launch_projectile()

            elif state == "game_over" and play_button.collidepoint(event.pos):
                reset_run()

            elif state == "victory":
                # retour au menu
                state = "menu"

        elif state == "game" and event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == pygame.K_z:
                game.player.jump()

        elif state == "game" and event.type == pygame.KEYUP:
            game.pressed[event.key] = False

    # ----------------------------
    # DRAW / UPDATE
    # ----------------------------
    if state == "menu":
        # ---- MENU : vidéo en fond ----
        ret, frame = game.menu_video.read()
        if not ret:
            game.menu_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = game.menu_video.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        video_surf = pygame.surfarray.make_surface(frame)
        video_surf = pygame.transform.scale(video_surf, screen.get_size())
        screen.blit(video_surf, (0, 0))

        # Ombre du bouton
        shadow_button_rect = pygame.Rect(play_button.x + 5, play_button.y + 5, play_button.width, play_button.height)
        pygame.draw.rect(screen, (60, 30, 10), shadow_button_rect)

        # Bouton
        pygame.draw.rect(screen, (191, 0, 255), play_button)
        pygame.draw.rect(screen, (255, 255, 255), play_button, 3)

        # Titre + ombre
        shadow_text = title_font.render("AVATAR", True, (75, 0, 130))
        shadow_rect = shadow_text.get_rect(center=(1366 // 2 + 5, 185))
        screen.blit(shadow_text, shadow_rect)

        title_text = title_font.render("AVATAR", True, (148, 0, 211))
        title_rect = title_text.get_rect(center=(1366 // 2, 180))
        screen.blit(title_text, title_rect)

        # Sous-titre
        subtitle_text = font.render("Héritier des 4 Mondes", True, (255, 250, 205))
        subtitle_rect = subtitle_text.get_rect(center=(1366 // 2, 260))
        screen.blit(subtitle_text, subtitle_rect)

        # Texte bouton
        txt = button_font.render("Jouer", True, (255, 255, 255))
        screen.blit(txt, (play_button.x + 70, play_button.y + 25))

        hint = font.render("Clic sur 'Jouer' pour lancer le jeu", True, (255, 255, 255))
        screen.blit(hint, (480, 590))

    elif state == "game":
        # ---- GAME ----

        # 1) vitesse scroll par défaut
        bg_speed = 0

        # 2) gravité
        game.player.apply_gravity()

        # 3) déplacements + scroll lié
        if game.pressed.get(pygame.K_d) and game.player.rect.x < screen.get_width() - game.player.rect.width:
            bg_speed = 2
            if game.player.on_ground:
                game.player.move_right()
            else:
                game.player.move_air_right()

        elif game.pressed.get(pygame.K_q) and game.player.rect.x > 0:
            bg_speed = -2
            if game.player.on_ground:
                game.player.move_left()
            else:
                game.player.move_air_left()

        bg_x -= bg_speed

        # boucle du fond
        if bg_x <= -background.get_width():
            bg_x = 0
        elif bg_x >= background.get_width():
            bg_x = 0

        # dessiner le fond
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + background.get_width(), 0))

        # joueur
        screen.blit(game.player.image, game.player.rect)
        game.player.update_health_bar(screen)

        # projectiles
        game.player.all_projectiles.draw(screen)
        for projectile in list(game.player.all_projectiles):
            projectile.move()

        # ennemis
        game.all_ennemies.draw(screen)
        for ennemie in list(game.all_ennemies):
            if ennemie.health > 0:
                ennemie.move()
                ennemie.animate()
                ennemie.update_health_bar(screen)
            else:
                game.all_ennemies.remove(ennemie)

        # Texte explication règle
        if game.level_number == 1:
            help_text = font.render("Tuez tous les ennemis pour libérer ce royaume !", True, (255, 255, 255))
            screen.blit(help_text, (450, 700))

        # FIN DE VAGUE :
        # - Monde feu (level 3) -> tempête
        # - Autres mondes -> transition panneau
        if len(game.all_ennemies) == 0 and not comet_event_active:
            if game.level_number == FIRE_LEVEL:
                comet_event_active = True
                comet_event_timer = 0
                game.comet_spawn_timer = 0
                print("=== TEMPÊTE DE COMÈTES (MONDE DU FEU) ===")
            else:
                state = "transition"

        # TEMPÊTE
        if comet_event_active:
            alert_text = alert_font.render(
                "Attention ce monde est instable !", True, (255, 80, 0)
            )
            alert_rect = alert_text.get_rect(center=(1366 // 2, 90))

            # Fond semi-transparent derrière le texte
            alert_bg = pygame.Surface((alert_rect.width + 40, alert_rect.height + 20))
            alert_bg.set_alpha(160)  # transparence
            alert_bg.fill((30, 0, 0))  # rouge sombre

            screen.blit(
                alert_bg,
                (alert_rect.x - 20, alert_rect.y - 10)
            )
            screen.blit(alert_text, alert_rect)
            comet_event_timer += 1

            if comet_event_timer <= COMET_EVENT_DURATION:
                game.comet_spawn_timer += 1
                if game.comet_spawn_timer >= 20:
                    game.all_comets.add(Comet(game))
                    game.comet_spawn_timer = 0
            else:
                # fin tempête
                comet_event_active = False
                game.all_comets.empty()

                # niveau suivant
                game.level_number += 1
                if game.level_number > MAX_LEVEL:
                    state = "victory"
                else:
                    load_level(game.level_number)
                    game.player.rect.x = 100
                    game.spawn_wave(game.wave_size)
                    state = "game"

        # comètes
        game.all_comets.draw(screen)
        for comet in list(game.all_comets):
            comet.move()

        # UI
        remaining = len(game.all_ennemies)
        ui_text = font.render(f"Ennemis restants: {remaining}/{game.wave_size}", True, (255, 255, 255))
        screen.blit(ui_text, (10, 10))

        # Game over
        if game.player.health <= 0:
            state = "game_over"

    elif state == "transition":
        # fond
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + background.get_width(), 0))

        # aligner panneau au sol
        panel_rect.bottom = game.player.ground_y + 110

        # panneau
        pygame.draw.rect(screen, (238, 0, 255), panel_rect)
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, 3)

        panel_text = font.render("Direction", True, (255, 255, 255))
        panel_text2 = font.render("le monde suivant", True, (255, 255, 255))
        screen.blit(panel_text, (panel_rect.x + 45, panel_rect.y + 20))
        screen.blit(panel_text2, (panel_rect.x + 15, panel_rect.y + 50))

        # déplacement auto
        game.player.move_right()

        # joueur
        screen.blit(game.player.image, game.player.rect)

        # collision panneau -> niveau suivant ou victoire
        if game.player.rect.colliderect(panel_rect):
            game.level_number += 1

            if game.level_number > MAX_LEVEL:
                state = "victory"
            else:
                load_level(game.level_number)
                game.player.rect.x = 100
                game.spawn_wave(game.wave_size)
                state = "game"

    elif state == "game_over":
        screen.fill((0, 0, 0))
        game_over_text = title_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (380, 250))

        pygame.draw.rect(screen, (200, 80, 80), play_button)
        pygame.draw.rect(screen, (255, 255, 255), play_button, 3)

        txt_retry = button_font.render("Rejouer", True, (255, 255, 255))
        screen.blit(txt_retry, (play_button.x + 30, play_button.y + 18))

    elif state == "victory":
        # Fond sombre (pas noir pur)
        screen.fill((15, 10, 25))

        # --- Titre "VICTOIRE !" avec ombre (mêmes couleurs que l'accueil) ---
        shadow_text = title_font.render("VICTOIRE !", True, (75, 0, 130))  # violet sombre
        shadow_rect = shadow_text.get_rect(center=(1366 // 2 + 6, 240 + 6))
        screen.blit(shadow_text, shadow_rect)

        win_text = title_font.render("VICTOIRE !", True, (148, 0, 211))  # violet
        win_rect = win_text.get_rect(center=(1366 // 2, 240))
        screen.blit(win_text, win_rect)

        # --- Petite phrase ---
        msg = subtitle_font.render("Vous avez libéré tous les royaumes", True, (255, 250, 205))  # jaune clair
        msg_rect = msg.get_rect(center=(1366 // 2, 380))
        screen.blit(msg, msg_rect)

        # --- Bouton retour menu (style bouton accueil) ---
        victory_button = pygame.Rect(540, 520, 300, 80)

        shadow_button = pygame.Rect(victory_button.x + 5, victory_button.y + 5,
                                    victory_button.width, victory_button.height)
        pygame.draw.rect(screen, (60, 30, 10), shadow_button)  # ombre marron

        pygame.draw.rect(screen, (191, 0, 255), victory_button)  # violet fluo
        pygame.draw.rect(screen, (255, 255, 255), victory_button, 3)

        txt = button_font.render("Menu", True, (255, 255, 255))
        txt_rect = txt.get_rect(center=victory_button.center)
        screen.blit(txt, txt_rect)


    # ----------------------------
    # FLIP + FPS
    # ----------------------------
    pygame.display.flip()
    clock.tick(60)
