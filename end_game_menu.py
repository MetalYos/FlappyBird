import pygame
import os
from settings import Settings
from button import Button
from helpers import draw_text


class EndGameMenu():
    def __init__(self, center_x, center_y, cached_fonts):
        self.score_menu_img = pygame.image.load(
            os.path.join('images', 'score_menu.png'))
        self.x = center_x - self.score_menu_img.get_width() // 2
        self.y = center_y - self.score_menu_img.get_height() // 2
        self.cached_fonts = cached_fonts
        self.on_restart_callback = None
        self.restart_params = None
        self.on_save_score_callback = None
        self.save_score_params = None

        self.init_gui()

    def init_gui(self):
        self.window_width = Settings.instance().settings['window_width']
        self.window_height = Settings.instance().settings['window_height']

        # load Score menu image
        self.score_menu_img = pygame.image.load(
            os.path.join('images', 'score_menu.png'))

        # Load and set restart button
        self.restart_button = Button(0, 0, os.path.join(
            'images', 'button_restart.png'), os.path.join('images', 'button_restart_clicked.png'))
        x = self.window_width // 2 - self.restart_button.width // 2
        y = self.window_height // 3 + self.score_menu_img.get_height() // 2 + \
            self.restart_button.height // 2
        self.restart_button.set_position(x, y)

        # Load and set save score button
        self.save_score_button = Button(0, 0, os.path.join(
            'images', 'button_save_score.png'), os.path.join('images', 'button_save_score_clicked.png'))
        x = self.window_width // 2 - \
            self.save_score_button.width // 2
        y = self.restart_button.y + self.restart_button.height + \
            self.save_score_button.height // 2
        self.save_score_button.set_position(x, y)

    def set_on_restart_callback(self, on_restart_callback, restart_params=None):
        self.restart_button.set_mouse_callback(
            on_restart_callback, restart_params)

    def set_on_save_score_callback(self, on_save_score_callback, save_score_params=None):
        self.save_score_button.set_mouse_callback(
            on_save_score_callback, save_score_params)

    def on_mouse_move(self, mouse_pos):
        self.restart_button.on_mouse_move(mouse_pos)
        self.save_score_button.on_mouse_move(mouse_pos)

    def on_mouse_click(self, mouse_pos):
        self.restart_button.on_mouse_click(mouse_pos)
        self.save_score_button.on_mouse_click(mouse_pos)

    def render(self, render_screen, score, highest_score):
        x = self.x
        y = self.y

        # Show lose menu
        render_screen.blit(self.score_menu_img, (x, y))

        # show bird score
        draw_text(render_screen, 'Score', self.cached_fonts['retro_20'], (255, 134, 45), True, pygame.Rect(
            x, y, self.score_menu_img.get_width(), self.score_menu_img.get_height() // 4), 'center', 'center')
        y = y + self.score_menu_img.get_height() // 4
        draw_text(render_screen, str(score), self.cached_fonts['retro_20'], (255, 134, 45), True, pygame.Rect(
            x, y, self.score_menu_img.get_width(), self.score_menu_img.get_height() // 4), 'center', 'center')

        # show bird high score
        y = y + self.score_menu_img.get_height() // 4
        draw_text(render_screen, 'Best', self.cached_fonts['retro_20'], (255, 134, 45), True, pygame.Rect(
            x, y, self.score_menu_img.get_width(), self.score_menu_img.get_height() // 4), 'center', 'center')
        y = y + self.score_menu_img.get_height() // 4
        draw_text(render_screen, str(highest_score), self.cached_fonts['retro_20'], (255, 134, 45), True, pygame.Rect(
            x, y, self.score_menu_img.get_width(), self.score_menu_img.get_height() // 4), 'center', 'center')

        # Show Restart button
        self.restart_button.render(render_screen)

        # Show Highscores button
        self.save_score_button.render(render_screen)
