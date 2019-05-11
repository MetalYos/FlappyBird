import pygame
import os
from constants import GROUND_HEIGHT, BG_BOTTOM_SCROLL_SPEED


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
        self.bottom_pipe_y = GROUND_HEIGHT + bottom_pipe_height
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
        self.x = self.x - int(BG_BOTTOM_SCROLL_SPEED * dt)

    def render(self, render_screen):
        render_screen.blit(self.bottom_pipe_img, (self.x, self.bottom_pipe_y))
        render_screen.blit(self.top_pipe_img, (self.x, self.top_pipe_y))
