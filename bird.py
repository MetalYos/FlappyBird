import pygame
import os
from settings import Settings
from helpers import draw_rotated_image


class Bird():
    def __init__(self, center_x, center_y):
        self.img = pygame.image.load(os.path.join('images', 'flappy_bird.png'))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.init_x = center_x - self.width // 2
        self.init_y = center_y - self.height // 2

        self.reset()

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y
        self.dy = 0
        self.d_angle = 0
        self.rot_rect = self.img.get_rect(topleft=(self.x, self.y))
        self.radius = 40
        self.score = 0
        self.highest_score = 0

    def left(self):
        return self.rot_rect.left

    def right(self):
        return self.rot_rect.right

    def top(self):
        return self.rot_rect.top

    def bottom(self):
        return self.rot_rect.bottom

    def increase_score(self):
        self.score += 1
        self.highest_score = max(self.highest_score, self.score)

    def update(self, dt):
        self.dy += Settings.instance().settings['gravity'] * dt
        self.y += self.dy

        if self.dy > Settings.instance().settings['fall_rot_threshold']:
            t = pygame.time.get_ticks() / 1000
            self.d_angle = max(-90,  self.d_angle + -
                               Settings.instance().settings['rot_speed'] * dt)

    def jump(self):
        self.dy = -Settings.instance().settings['jump_force']
        self.d_angle = 0

    def render(self, render_screen):
        self.rot_rect = self.rotated_image = draw_rotated_image(render_screen, self.img, (self.x, self.y),
                                                                (self.width // 2, self.height // 2), self.d_angle)
