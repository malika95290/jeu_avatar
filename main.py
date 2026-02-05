import pygame
import cv2
import numpy as np

from Game import Game
from Comet import Comet

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MAX_LEVEL, FIRE_LEVEL,
    THEME_BG, WHITE,
    COMET_EVENT_DURATION
)
from ui_manager import UIManager
from settings_manager import SettingsManager
from level_manager import LevelManager

# ----------------------------
# INIT
# ----------------------------
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("World of Fire")
clock = pygame.time.Clock()

game = Game()
settings = SettingsManager()
ui = UIManager()
levels = LevelManager(game, screen, settings)

# ----------------------------
# STATES
# ----------------------------
state = "menu"     
paused = False

# ----------------------------
# UI RECTANGLES
# ----------------------------
play_button = pygame.Rect(560, 500, 250, 80)
settings_button = pygame.Rect(560, 600, 250, 80)

# SETTINGS SCREEN
back_button = pygame.Rect(40, 40, 180, 60)
shoot_mouse_btn = pygame.Rect(460, 220, 420, 70)
shoot_space_btn = pygame.Rect(460, 310, 420, 70)
move_qd_btn = pygame.Rect(460, 430, 420, 70)
move_arrows_btn = pygame.Rect(460, 520, 420, 70)
pause_key_btn = pygame.Rect(460, 640, 420, 70)

vol_bar = pygame.Rect(460, 140, 420, 18)
vol_knob_w = 18
dragging_volume = False
waiting_for_pause_key = False

# TRANSITION PANEL
panel_rect = pygame.Rect(1100, 0, 240, 100)

# PAUSE BUTTON
quit_app_button = pygame.Rect(533, 480, 300, 70)

# ----------------------------
# COMET EVENT
# ----------------------------
comet_event_active = False
comet_event_timer = 0

# ----------------------------
# START LEVEL 1
# ----------------------------
game.level_number = 1
levels.load_level(game.level_number)

def reset_run():
    global state, paused, comet_event_active, comet_event_timer

    state = "game"
    paused = False
    game.pressed = {}

    game.player.health = game.player.max_health
    game.player.rect.x = 100

    game.all_comets.empty()
    game.all_ennemies.empty()

    comet_event_active = False
    comet_event_timer = 0
    game.comet_spawn_timer = 0

    game.level_number = 1
    levels.load_level(game.level_number)

    game.spawn_wave(game.wave_size)

# ----------------------------
# MAIN LOOP
# ----------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # ----------------------------
        # MOUSE CLICK
        # ----------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # MENU
            if state == "menu":
                if play_button.collidepoint(event.pos):
                    reset_run()
                elif settings_button.collidepoint(event.pos):
                    state = "settings"

            # SETTINGS
            elif state == "settings":
                if back_button.collidepoint(event.pos):
                    state = "menu"
                    waiting_for_pause_key = False
                    dragging_volume = False

                elif shoot_mouse_btn.collidepoint(event.pos):
                    settings.settings["shoot_mode"] = "mouse"
                elif shoot_space_btn.collidepoint(event.pos):
                    settings.settings["shoot_mode"] = "space"

                elif move_qd_btn.collidepoint(event.pos):
                    settings.settings["move_mode"] = "qd"
                elif move_arrows_btn.collidepoint(event.pos):
                    settings.settings["move_mode"] = "arrows"

                elif pause_key_btn.collidepoint(event.pos):
                    waiting_for_pause_key = True

                elif vol_bar.collidepoint(event.pos):
                    dragging_volume = True
                    rel_x = event.pos[0] - vol_bar.x
                    settings.set_music_volume(rel_x / vol_bar.w)

            # GAME
            elif state == "game":
                # Si pause + clic sur quitter
                if paused and quit_app_button.collidepoint(event.pos):
                    running = False
                    pygame.quit()

                # Tir clic gauche 
                elif not paused and settings.settings["shoot_mode"] == "mouse":
                    game.player.launch_projectile()

            # GAME OVER
            elif state == "game_over":
                if play_button.collidepoint(event.pos):
                    reset_run()

            # VICTORY
            elif state == "victory":
                state = "menu"

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging_volume = False

        elif event.type == pygame.MOUSEMOTION:
            if state == "settings" and dragging_volume:
                rel_x = event.pos[0] - vol_bar.x
                settings.set_music_volume(rel_x / vol_bar.w)

        # ----------------------------
        # KEYBOARD
        # ----------------------------
        elif event.type == pygame.KEYDOWN:
            # SETTINGS : choisir la touche pause
            if state == "settings" and waiting_for_pause_key:
                settings.settings["pause_key"] = event.key
                waiting_for_pause_key = False

            elif state == "game":
                game.pressed[event.key] = True

                # pause
                if event.key == settings.settings["pause_key"]:
                    paused = not paused

                # tir au clavier (espace)
                if (not paused) and settings.settings["shoot_mode"] == "space":
                    if event.key == pygame.K_SPACE:
                        game.player.launch_projectile()

                # saut
                if (not paused) and event.key == pygame.K_z:
                    game.player.jump()

        elif event.type == pygame.KEYUP:
            if state == "game":
                game.pressed[event.key] = False

    # ----------------------------
    # DRAW / UPDATE
    # ----------------------------

    # ============ MENU ============
    if state == "menu":
        ret, frame = game.menu_video.read()
        if not ret:
            game.menu_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = game.menu_video.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        video_surf = pygame.surfarray.make_surface(frame)
        video_surf = pygame.transform.scale(video_surf, screen.get_size())
        screen.blit(video_surf, (0, 0))

        ui.draw_title_with_shadow(screen, "AVATAR", SCREEN_WIDTH // 2, 180)

        subtitle_text = ui.font.render("Héritier des 4 Mondes", True, (255, 250, 205))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
        screen.blit(subtitle_text, subtitle_rect)

        ui.draw_button(screen, play_button, "Jouer")
        ui.draw_button(screen, settings_button, "Paramètres")

    # ============ SETTINGS ============
    elif state == "settings":
        screen.fill(THEME_BG)

        t = ui.subtitle_font.render("PARAMÈTRES", True, (255, 250, 205))
        screen.blit(t, (500, 40))

        ui.draw_small_button(screen, back_button, "RETOUR")

        # Volume
        vol_label = ui.font.render("Volume musique", True, WHITE)
        screen.blit(vol_label, (460, 95))

        pygame.draw.rect(screen, WHITE, vol_bar, 2)

        knob_x = vol_bar.x + int(settings.settings["music_volume"] * vol_bar.w) - (vol_knob_w // 2)
        knob_rect = pygame.Rect(knob_x, vol_bar.y - 8, vol_knob_w, vol_bar.h + 16)
        pygame.draw.rect(screen, (191, 0, 255), knob_rect)
        pygame.draw.rect(screen, WHITE, knob_rect, 2)

        vol_pct = ui.font.render(f"{int(settings.settings['music_volume'] * 100)}%", True, WHITE)
        screen.blit(vol_pct, (900, 132))

        # Tir
        label_shoot = ui.font.render("Tir", True, WHITE)
        screen.blit(label_shoot, (460, 185))

        ui.draw_small_button(screen, shoot_mouse_btn, "Clic gauche", active=(settings.settings["shoot_mode"] == "mouse"))
        ui.draw_small_button(screen, shoot_space_btn, "Espace", active=(settings.settings["shoot_mode"] == "space"))

        # Déplacement
        label_move = ui.font.render("Gauche / Droite", True, WHITE)
        screen.blit(label_move, (460, 395))

        ui.draw_small_button(screen, move_qd_btn, "Q / D", active=(settings.settings["move_mode"] == "qd"))
        ui.draw_small_button(screen, move_arrows_btn, "Flèches", active=(settings.settings["move_mode"] == "arrows"))

        # Pause
        label_pause = ui.font.render("Pause", True, WHITE)
        screen.blit(label_pause, (460, 605))

        pause_text = f"Touche : {ui.key_name(settings.settings['pause_key'])}"
        if waiting_for_pause_key:
            pause_text = "Appuie sur une touche..."
        ui.draw_small_button(screen, pause_key_btn, pause_text, active=waiting_for_pause_key)

    # ============ GAME ============
    elif state == "game":
        bg_speed = 0

        if not paused:
            game.player.apply_gravity()

            left_key, right_key = settings.get_move_keys()

            if game.pressed.get(right_key) and game.player.rect.x < SCREEN_WIDTH - game.player.rect.width:
                bg_speed = 2
                if game.player.on_ground:
                    game.player.move_right()
                else:
                    game.player.move_air_right()

            elif game.pressed.get(left_key) and game.player.rect.x > 0:
                bg_speed = -2
                if game.player.on_ground:
                    game.player.move_left()
                else:
                    game.player.move_air_left()

        # background
        levels.draw_scrolling_background(bg_speed)

        # player
        screen.blit(game.player.image, game.player.rect)
        game.player.update_health_bar(screen)

        if not paused:
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

            # fin vague
            if len(game.all_ennemies) == 0 and not comet_event_active:
                if game.level_number == FIRE_LEVEL:
                    comet_event_active = True
                    comet_event_timer = 0
                    game.comet_spawn_timer = 0
                else:
                    state = "transition"

            # tempête
            if comet_event_active:
                alert_text = ui.alert_font.render("Attention ce monde est instable !", True, (255, 80, 0))
                alert_rect = alert_text.get_rect(center=(SCREEN_WIDTH // 2, 90))

                alert_bg = pygame.Surface((alert_rect.width + 40, alert_rect.height + 20))
                alert_bg.set_alpha(160)
                alert_bg.fill((30, 0, 0))

                screen.blit(alert_bg, (alert_rect.x - 20, alert_rect.y - 10))
                screen.blit(alert_text, alert_rect)

                comet_event_timer += 1
                if comet_event_timer <= COMET_EVENT_DURATION:
                    game.comet_spawn_timer += 1
                    if game.comet_spawn_timer >= 20:
                        game.all_comets.add(Comet(game))
                        game.comet_spawn_timer = 0
                else:
                    comet_event_active = False
                    game.all_comets.empty()

                    game.level_number += 1
                    if game.level_number > MAX_LEVEL:
                        state = "victory"
                    else:
                        levels.load_level(game.level_number)
                        game.player.rect.x = 100
                        game.spawn_wave(game.wave_size)
                        state = "game"

            # comètes
            game.all_comets.draw(screen)
            for comet in list(game.all_comets):
                comet.move()

            # UI simple
            remaining = len(game.all_ennemies)
            ui_text = ui.font.render(f"Ennemis restants: {remaining}/{game.wave_size}", True, WHITE)
            screen.blit(ui_text, (10, 10))

            if game.player.health <= 0:
                state = "game_over"

        else:
            # affichage en pause 
            game.player.all_projectiles.draw(screen)
            game.all_ennemies.draw(screen)
            game.all_comets.draw(screen)

            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(140)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            pause_txt = ui.title_font.render("PAUSE", True, WHITE)
            pause_rect = pause_txt.get_rect(center=(SCREEN_WIDTH // 2, 300))
            screen.blit(pause_txt, pause_rect)

            help_pause = ui.font.render(
                f"Appuyer {ui.key_name(settings.settings['pause_key'])} pour reprendre le jeu",
                True, WHITE
            )
            help_rect = help_pause.get_rect(center=(SCREEN_WIDTH // 2, 420))
            screen.blit(help_pause, help_rect)

            # bouton quitter
            ui.draw_button(screen, quit_app_button, "Quitter l'appli")

    # ============ TRANSITION ============
    elif state == "transition":
        # background fixe (tu peux garder le scroll si tu veux, mais simple = fixe)
        screen.blit(levels.background, (0, 0))

        panel_rect.bottom = game.player.ground_y + 110

        pygame.draw.rect(screen, (238, 0, 255), panel_rect)
        pygame.draw.rect(screen, WHITE, panel_rect, 3)

        panel_text = ui.font.render("Direction", True, WHITE)
        panel_text2 = ui.font.render("le monde suivant", True, WHITE)
        screen.blit(panel_text, (panel_rect.x + 45, panel_rect.y + 20))
        screen.blit(panel_text2, (panel_rect.x + 15, panel_rect.y + 50))

        game.player.move_right()
        screen.blit(game.player.image, game.player.rect)

        if game.player.rect.colliderect(panel_rect):
            game.level_number += 1
            if game.level_number > MAX_LEVEL:
                state = "victory"
            else:
                levels.load_level(game.level_number)
                game.player.rect.x = 100
                game.spawn_wave(game.wave_size)
                state = "game"

    # ============ GAME OVER ============
    elif state == "game_over":
        screen.fill(THEME_BG)

        # texte centré
        ui.draw_title_with_shadow(screen, "GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)

        # bouton rejouer centré
        play_button.size = (300, 80)
        play_button.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        ui.draw_button(screen, play_button, "Rejouer")

    # ============ VICTORY ============
    elif state == "victory":
        screen.fill(THEME_BG)
        ui.draw_title_with_shadow(screen, "VICTOIRE !", SCREEN_WIDTH // 2, 240)

        msg = ui.subtitle_font.render("Vous avez libéré tous les royaumes", True, (255, 250, 205))
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, 380))
        screen.blit(msg, msg_rect)

        info = ui.font.render("Clique pour revenir au menu", True, WHITE)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, 460))
        screen.blit(info, info_rect)

    pygame.display.flip()
    clock.tick(60)
