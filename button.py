import pygame


class Button():
    def __init__(self, x, y, img_path, pressed_img_path):
        self.scale_factor = 6
        self.set_position(x, y)
        self.img = pygame.image.load(img_path)
        self.pressed_img = pygame.image.load(pressed_img_path)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.current_img = self.img
        self.callback_func = None

    def set_position(self, x, y):
        self.init_x = x
        self.init_y = y
        self.scaled_x = self.init_x - self.scale_factor // 2
        self.scaled_y = self.init_y - self.scale_factor // 2
        self.x = self.init_x
        self.y = self.init_y

    def set_mouse_callback(self, callback_func, func_params):
        self.callback_func = callback_func
        self.func_params = func_params

    def render(self, render_screen):
        render_screen.blit(self.current_img, (self.x, self.y))

    def contains_point(self, point):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return rect.collidepoint(point)

    def on_mouse_move(self, mouse_pos):
        if self.contains_point(mouse_pos):
            self.current_img = pygame.transform.scale(
                self.pressed_img, (self.width + self.scale_factor, self.height + self.scale_factor))
            self.x = self.scaled_x
            self.y = self.scaled_y
        else:
            self.current_img = self.img
            self.x = self.init_x
            self.y = self.init_y

    def on_mouse_click(self, mouse_pos):
        if self.contains_point(mouse_pos):
            if self.callback_func is not None:
                if self.func_params is None:
                    self.callback_func()
                else:
                    self.callback_func(self.func_params)
