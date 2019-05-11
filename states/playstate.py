import pygame
import random
import statemachine
from states.basestate import BaseState
from helpers import draw_text
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from scrolling_background import ScrollingBackground


class PlayState(BaseState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_params=None):
        self.background = ScrollingBackground(
            'images\\background_tile.png', 0, 5, 100, WINDOW_WIDTH)
        self.scroll_speed = 5

    def exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        # Update scrolling background
        self.background.update(dt)

    def render(self, render_screen):
        # Draw scrolling background
        self.background.render(render_screen)

        # Draw bird

        # Draw Pipes
        pass

    def on_keypress(self, dt):
        pass

    def on_mouse_move(self):
        pass
