import pygame
import random
import statemachine
from states.basestate import BaseState


class PlayState(BaseState):
    def __init__(self):
        super().__init__()

    def enter(self, enter_params=None):
        pass

    def exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, render_screen):
        pass

    def on_keypress(self, dt):
        pass

    def on_mouse_move(self):
        pass
