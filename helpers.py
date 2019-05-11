import pygame
import os


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


def load_font(path, name, fonts, size):
    font = fonts.get(name)
    if font is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        font = pygame.font.Font(canonicalized_path, size)
        fonts[name] = font


def load_sound(path, name, sounds):
    sound = sounds.get(name)
    if sound is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        sounds[name] = sound


def play_music(index, music_list):
    if index < 0 or index >= len(music_list):
        return

    canonicalized_path = music_list[index].replace(
        '/', os.sep).replace('\\', os.sep)
    pygame.mixer.music.load(canonicalized_path)
    pygame.mixer.music.play(-1)


def draw_text(render_screen, text, font, color, antialias, align_rect, h_aligh='center', v_aligh='center'):
    text_render = font.render(text, antialias, color)
    # Horizontal align (default = center)
    pos_x = align_rect.x + align_rect.width // 2 - text_render.get_width() // 2
    if h_aligh is 'left':
        pos_x = align_rect.x
    if h_aligh is 'right':
        pos_x = align_rect.x + align_rect.width - text_render.get_width()

    # Vertical align (default = center)
    pos_y = align_rect.y + align_rect.height // 2 - text_render.get_height() // 2
    if v_aligh == 'top':
        pos_y = align_rect.y
    if v_aligh is 'bottom':
        pos_y = align_rect.y + align_rect.height - text_render.get_height()

    render_screen.blit(text_render, (pos_x, pos_y))


def draw_rotated_image(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[
               0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[
               0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0],
              pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)
