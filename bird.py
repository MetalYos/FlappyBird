import pygame
import os
from constants import *
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
        self.rot_rect = self.img.get_rect(topleft=(self.x, self.y))

        self.score = 0

    def left(self):
        return self.rot_rect.left

    def right(self):
        return self.rot_rect.right

    def top(self):
        return self.rot_rect.top

    def bottom(self):
        return self.rot_rect.bottom

    def update(self, dt):
        self.dy += GRAVITY * dt
        self.y += self.dy

        if self.dy > FALL_ROT_THRESHOLD:
            t = pygame.time.get_ticks() / 1000
            self.d_angle = max(-90,  self.d_angle + -ROT_SPEED * dt)

    def jump(self):
        self.dy = -JUMP_FORCE
        self.d_angle = JUMP_ROT_ANGLE

    def collides(self, pipe_pair):
        if self.left() > pipe_pair.right():
            return False

        if self.right() < pipe_pair.left():
            return False

        if self.top() + PIPE_HIT_TOP_TOLERANCE <= pipe_pair.top_pipe_bottom():
            if self.right() - self.rot_rect.width // 2 >= pipe_pair.left():
                print('First Coll')
                return True

        if self.bottom() - PIPE_HIT_BOTTOM_TOLERANCE >= pipe_pair.bottom_pipe_top():
            if self.right() - self.rot_rect.width // 2 >= pipe_pair.left():
                return True

        return False

    def render(self, render_screen):
        self.rot_rect = self.rotated_image = draw_rotated_image(render_screen, self.img, (self.x, self.y),
                                                                (self.width // 2, self.height // 2), self.d_angle)
