import pygame
import os
import random
import statemachine
from states.basestate import BaseState
from helpers import draw_text, load_font
from settings import Settings
from scrolling_background import ScrollingBackground
from bird import Bird
from pipe_pair import PipePair
from button import Button
from end_game_menu import EndGameMenu


class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.play = False
        self.lose = False
        self.pipe_pairs = []
        self.next_pipe_index = 0

    def enter(self, enter_params=None):
        self.window_width = Settings.instance().settings['window_width']
        self.window_height = Settings.instance().settings['window_height']
        self.far_scroll_speed = Settings.instance(
        ).settings['far_scroll_speed']
        self.close_scroll_speed = Settings.instance(
        ).settings['close_scroll_speed']
        self.pipe_horizontal_gap = Settings.instance(
        ).settings['pipe_horizontal_gap']
        self.pipe_min_height = Settings.instance(
        ).settings['pipe_min_height']
        self.pipe_max_height = Settings.instance(
        ).settings['pipe_max_height']
        self.pipe_gap_min = Settings.instance(
        ).settings['pipe_gap_min']
        self.pipe_gap_max = Settings.instance(
        ).settings['pipe_gap_max']

        # Load fonts
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_70', self.cached_fonts, 70)
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_40', self.cached_fonts, 40)
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_20', self.cached_fonts, 20)
        load_font(os.path.join('fonts', 'super_retro.ttf'),
                  'retro_10', self.cached_fonts, 10)

        # Load background images
        self.background_top = ScrollingBackground(
            os.path.join('images', 'background_top_tile.png'), 0, 5,
            self.far_scroll_speed, self.window_width)

        self.background_bottom = ScrollingBackground(
            os.path.join('images', 'background_bottom_tile.png'), 0, 5,
            self.close_scroll_speed, self.window_width)
        self.background_bottom.y = self.window_height - \
            self.background_bottom.tile_image.get_height()

        # Load score menu
        self.end_game_menu = EndGameMenu(
            self.window_width // 2, self.window_height // 3, self.cached_fonts)
        self.end_game_menu.set_on_restart_callback(self.new_game)

        # Load bird
        self.bird = Bird(self.window_width // 2, self.window_height // 2)

        self.new_game()

    def exit(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    statemachine.StateMachine.instance().exit()
                if event.key == pygame.K_SPACE:
                    if not self.play and not self.lose:
                        self.play = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and self.lose:
                    self.end_game_menu.on_mouse_click(event.pos)

    def update(self, dt):
        # Update scrolling background
        self.background_top.update(dt)
        self.background_bottom.update(dt)

        if self.play:
            # Update bird (gravity)
            self.bird.update(dt)

            # Update pipes
            for pipe_pair in self.pipe_pairs:
                pipe_pair.update(dt)

            # Check collision with pipes
            if self.pipe_pairs[self.next_pipe_index].collides(self.bird):
                self.play = False
                self.lose = True
                return

            # Check collision with ground
            if self.bird.bottom() >= Settings.instance().settings['window_height'] - Settings.instance().settings['ground_height']:
                self.play = False
                self.lose = True
                return

            # if bird passed the pair of pipes, add a point
            if self.bird.left() >= self.pipe_pairs[self.next_pipe_index].right():
                self.bird.increase_score()
                self.next_pipe_index += 1

            # Spawn pipe pair if needed
            if self.pipe_pairs[-1].left() <= self.window_width:
                pipe_pair = PipePair(self.window_width + self.pipe_horizontal_gap,
                                     random.randint(
                                         self.pipe_min_height, self.pipe_max_height),
                                     random.randint(self.pipe_gap_min, self.pipe_gap_max))
                self.pipe_pairs.append(pipe_pair)

            # Remove the first pair if needed
            if self.pipe_pairs[0].right() < 0:
                self.pipe_pairs.pop(0)
                pipe_pair = PipePair(self.pipe_pairs[-1].right() + self.pipe_horizontal_gap,
                                     random.randint(
                                         self.pipe_min_height, self.pipe_max_height),
                                     random.randint(self.pipe_gap_min, self.pipe_gap_max))
                self.pipe_pairs.append(pipe_pair)
                self.next_pipe_index -= 1

        self.on_keypress(dt)
        self.on_mouse_move()

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

        if not self.play and not self.lose:
            # Draw welcome message
            draw_text(render_screen, 'Welcome to Flappy Yos!', self.cached_fonts['retro_70'], (255, 255, 255), True, pygame.Rect(
                0, self.window_height // 9, self.window_width, self.window_height - self.window_height // 9), 'center', 'top')
            draw_text(render_screen, 'Press Spacebar to start playing', self.cached_fonts['retro_40'], (255, 255, 255), True, pygame.Rect(
                0, self.window_height // 4, self.window_width, self.window_height - self.window_height // 4), 'center', 'top')
        if self.play:
            # Draw score
            draw_text(render_screen, str(self.bird.score), self.cached_fonts['retro_70'], (255, 255, 255), True, pygame.Rect(
                0, self.window_height // 8, self.window_width, self.window_height - self.window_height // 8), 'center', 'top')
        if self.lose:
            self.end_game_menu.render(
                render_screen, self.bird.score, self.bird.highest_score)

    def on_keypress(self, dt):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.play:
            self.bird.jump()

    def on_mouse_move(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.lose:
            self.end_game_menu.on_mouse_move(mouse_pos)

    def new_game(self):
        self.bird.reset()
        self.pipe_pairs = []

        # Load first Pipe Pair
        pipe_pair = PipePair(self.window_width + self.pipe_horizontal_gap,
                             random.randint(self.pipe_min_height,
                                            self.pipe_max_height),
                             random.randint(self.pipe_gap_min, self.pipe_gap_max))
        self.pipe_pairs.append(pipe_pair)
        self.next_pipe_index = 0

        self.play = False
        self.lose = False
