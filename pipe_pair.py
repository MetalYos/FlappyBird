import pygame
import os
import math
from settings import Settings


class PipePair():
    def __init__(self, bottom_pipe_center_x, bottom_pipe_height, gap):
        self.bottom_pipe_img = pygame.image.load(
            os.path.join('images', 'pipe.png'))
        self.top_pipe_img = pygame.image.load(
            os.path.join('images', 'pipe.png'))
        self.top_pipe_img = pygame.transform.flip(
            self.top_pipe_img, False, True)
        self.width = self.bottom_pipe_img.get_width()
        self.x = bottom_pipe_center_x - self.width
        self.gap = gap
        self.bottom_pipe_y = Settings.instance(
        ).settings['ground_height'] + bottom_pipe_height
        self.top_pipe_y = self.bottom_pipe_y - gap - self.top_pipe_img.get_height()

    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def bottom_pipe_top(self):
        return self.bottom_pipe_y

    def top_pipe_bottom(self):
        return self.bottom_pipe_y - self.gap

    def update(self, dt):
        self.x = self.x - \
            int(Settings.instance().settings['close_scroll_speed'] * dt)

    def collides(self, bird):
        radius = bird.radius
        center = (bird.x, bird.y)

        # check top pipe bottom edge
        for x in range(self.left(), self.right()):
            distance = math.sqrt(
                (x - center[0])**2 + (self.top_pipe_bottom() - center[1])**2)
            if distance < radius:
                return True

        # Check bottom pipe top edge
        for x in range(self.left(), self.right()):
            distance = math.sqrt(
                (x - center[0])**2 + (self.bottom_pipe_top() - center[1])**2)
            if distance < radius:
                return True

        # Check top left edge
        for y in range(self.top_pipe_bottom()):
            distance = math.sqrt(
                (self.left() - center[0])**2 + (y - center[1])**2)
            if distance < radius:
                return True

        # Check bottom left edge
        for y in range(self.bottom_pipe_top(),
                       Settings.instance().settings['window_height'] - Settings.instance().settings['ground_height']):
            distance = math.sqrt(
                (self.left() - center[0])**2 + (y - center[1])**2)
            if distance < radius:
                return True

        return False

    def render(self, render_screen):
        render_screen.blit(self.bottom_pipe_img, (self.x, self.bottom_pipe_y))
        render_screen.blit(self.top_pipe_img, (self.x, self.top_pipe_y))
