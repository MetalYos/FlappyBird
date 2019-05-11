import pygame
import os
import random
import statemachine
from states.basestate import BaseState
from helpers import draw_text, load_font
from constants import *
from scrolling_background import ScrollingBackground
from bird import Bird
from pipe_pair import PipePair


class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.start = False
        self.pipe_pairs = []
        self.next_pipe_index = 0

    def enter(self, enter_params=None):
        # Load fonts
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_70', self.cached_fonts, 70)
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_40', self.cached_fonts, 40)
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_10', self.cached_fonts, 10)

        # Load background images
        self.background_top = ScrollingBackground(
            os.path.join('images', 'background_top_tile.png'), 0, 5, BG_TOP_SCROLL_SPEED, WINDOW_WIDTH)

        self.background_bottom = ScrollingBackground(
            os.path.join('images', 'background_bottom_tile.png'), 0, 5, BG_BOTTOM_SCROLL_SPEED, WINDOW_WIDTH)
        self.background_bottom.y = WINDOW_HEIGHT - \
            self.background_bottom.tile_image.get_height()

        # Load bird
        self.bird = Bird(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Load first Pipe Pair
        pipe_pair = PipePair(WINDOW_WIDTH + PIPE_HORIZONTAL_GAP,
                             random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT), random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX))
        self.pipe_pairs.append(pipe_pair)

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

            # Update pipes
            for pipe_pair in self.pipe_pairs:
                pipe_pair.update(dt)

            # Check collision with pipes
            if self.bird.collides(self.pipe_pairs[self.next_pipe_index]):
                self.start = False

            # if bird passed the pair of pipes, add a point
            if self.bird.left() >= self.pipe_pairs[self.next_pipe_index].right():
                self.bird.score += 1
                self.next_pipe_index += 1

            # Spawn pipe pair if needed
            if self.pipe_pairs[-1].left() <= WINDOW_WIDTH:
                pipe_pair = PipePair(WINDOW_WIDTH + PIPE_HORIZONTAL_GAP,
                                     random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT), random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX))
                self.pipe_pairs.append(pipe_pair)

            # Remove the first pair if needed
            if self.pipe_pairs[0].right() < 0:
                self.pipe_pairs.pop(0)
                pipe_pair = PipePair(self.pipe_pairs[-1].right() + PIPE_HORIZONTAL_GAP,
                                     random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT), random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX))
                self.pipe_pairs.append(pipe_pair)
                self.next_pipe_index -= 1

        self.on_keypress(dt)

    def render(self, render_screen):
        # Draw scrolling top background
        self.background_top.render(render_screen)

        # Draw Pipes
        for pipe_pair in self.pipe_pairs:
            pipe_pair.render(render_screen)

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

        mouse_pos = pygame.mouse.get_pos()
        text_render = self.cached_fonts['retro_10'].render(
            f'({mouse_pos[0]}, {mouse_pos[1]})', True, (255, 255, 255))
        render_screen.blit(text_render, mouse_pos)

    def on_keypress(self, dt):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            self.start = True
            self.bird.jump()

    def on_mouse_move(self):
        pass
