import pygame
import os
import statemachine
from states.basestate import BaseState
from helpers import draw_text, load_font
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BG_TOP_SCROLL_SPEED, BG_BOTTOM_SCROLL_SPEED
from scrolling_background import ScrollingBackground
from bird import Bird


class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.start = False

    def enter(self, enter_params=None):
        # Load fonts
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_70', self.cached_fonts, 70)
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_40', self.cached_fonts, 40)

        # Load background images
        self.background_top = ScrollingBackground(
            os.path.join('images', 'background_top_tile.png'), 0, 5, BG_TOP_SCROLL_SPEED, WINDOW_WIDTH)

        self.background_bottom = ScrollingBackground(
            os.path.join('images', 'background_bottom_tile.png'), 0, 5, BG_BOTTOM_SCROLL_SPEED, WINDOW_WIDTH)
        self.background_bottom.y = WINDOW_HEIGHT - \
            self.background_bottom.tile_image.get_height()

        # Load bird
        self.bird = Bird(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def exit(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    statemachine.StateMachine.instance().exit()

    def update(self, dt):
        # Update scrolling background
        self.background_top.update(dt)
        self.background_bottom.update(dt)

        if self.start:
            # Update bird (gravity)
            self.bird.update(dt)

        self.on_keypress(dt)

    def render(self, render_screen):
        # Draw scrolling top background
        self.background_top.render(render_screen)

        # Draw Pipes

        # Draw bird
        self.bird.render(render_screen)

        # Draw scrolling bottom background
        self.background_bottom.render(render_screen)

        # Draw score
        if not self.start:
            draw_text(render_screen, 'Press Spacebar to start playing', self.cached_fonts['retro_40'], (255, 255, 255), True, pygame.Rect(
                0, WINDOW_HEIGHT // 6, WINDOW_WIDTH, WINDOW_HEIGHT - WINDOW_HEIGHT // 6), 'center', 'top')
        else:
            draw_text(render_screen, str(self.bird.score), self.cached_fonts['retro_70'], (255, 255, 255), True, pygame.Rect(
                0, WINDOW_HEIGHT // 8, WINDOW_WIDTH, WINDOW_HEIGHT - WINDOW_HEIGHT // 8), 'center', 'top')

    def on_keypress(self, dt):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            self.start = True
            self.bird.jump()

    def on_mouse_move(self):
        pass
