import pygame


class ScrollingBackground():
    def __init__(self, img_tile_path, y, num_tiles, scroll_speed, screen_width, direction='right'):
        self.tile_image = pygame.image.load(img_tile_path)
        self.tile_image.convert_alpha()
        self.direction = direction

        self.init_x = -self.tile_image.get_width()
        if self.direction is 'right':
            self.init_x = 0

        self.y = y
        self.num_tiles = num_tiles
        self.scroll_speed = scroll_speed
        self.screen_width = screen_width
        self.restart = True
        self.pos_x = self.init_x

    def update(self, dt):
        if self.direction is 'left':
            self.pos_x = (self.pos_x + int(self.scroll_speed * dt))
        else:
            self.pos_x = (self.pos_x - int(self.scroll_speed * dt))

        if self.direction is 'left' and self.pos_x >= 0:
            self.pos_x = self.init_x
        if self.direction is 'right' and self.pos_x <= -self.tile_image.get_width():
            self.pos_x = self.init_x

    def render(self, render_screen):
        for i in range(self.num_tiles):
            pos_x = self.pos_x + i * self.tile_image.get_width()
            render_screen.blit(self.tile_image, (pos_x, self.y))
