import pygame
import random
from statemachine import StateMachine
from constants import *


class Game():
    def __init__(self):
        pygame.init()
        random.seed()
        self.render_screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.done = False

        StateMachine.instance().set_change('play', False)
        StateMachine.instance().change()

    def run(self):
        while not self.done:
            self.handle_events()
            self.update()
            self.render()
            StateMachine.instance().change()

            if StateMachine.instance().should_exit:
                self.done = True

        self.quit()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True

        StateMachine.instance().handle_events(events)

    def update(self):
        StateMachine.instance().update(self.dt)

    def render(self):
        # Fill render screen
        self.render_screen.fill((0, 0, 0))

        StateMachine.instance().render(self.render_screen)

        pygame.display.flip()
        self.dt = self.clock.tick(FPS) / 1000

    def quit(self):
        pass
