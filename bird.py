import pygame
import os
from constants import GRAVITY, JUMP_FORCE, JUMP_ROT_ANGLE, FALL_ROT_THRESHOLD, ROT_SPEED
from helpers import draw_rotated_image


class Bird():
    def __init__(self, center_x, center_y):
        self.img = pygame.image.load(os.path.join('images', 'flappy_bird.png'))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = center_x - self.width // 2
        self.y = center_y - self.height // 2
        self.dy = 0
        self.d_angle = 0
        self.rot_angle = 0

        self.score = 0

    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def update(self, dt):
        self.dy += GRAVITY * dt
        self.y += self.dy

        if self.dy > FALL_ROT_THRESHOLD:
            t = pygame.time.get_ticks() / 1000
            self.d_angle = max(-90,  self.d_angle + -ROT_SPEED * dt)

    def jump(self):
        self.dy = -JUMP_FORCE
        self.d_angle = JUMP_ROT_ANGLE

    def render(self, render_screen):
        #render_screen.blit(self.img, (self.x, self.y))
        draw_rotated_image(render_screen, self.img, (self.x, self.y),
                           (self.width // 2, self.height // 2), self.d_angle)
