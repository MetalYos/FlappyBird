from helpers import Singleton
from states.playstate import PlayState


@Singleton
class StateMachine():
    def __init__(self):
        self.states_stack = []
        self.current = None
        self.should_exit = False

        self.new_states = {
            'play': (lambda: PlayState()),
        }

        self.impending_change = {}

    def set_change(self, state_name, enter_params={}):
        if self.new_states.get(state_name) is None:
            return

        self.impending_change['current'] = self.new_states[state_name]()
        self.impending_change['enter_params'] = enter_params

    def change(self):
        if len(self.impending_change) == 0:
            return

        if self.current is not None:
            self.current.exit()

        self.current = self.impending_change['current']

        enter_params = self.impending_change.get('enter_params')
        if enter_params is not None:
            self.current.enter(enter_params)

        self.impending_change = {}

    def push(self, name, enter_params={}):
        if self.current is not None:
            self.states_stack.append(self.current)
            self.impending_change['current'] = self.new_states[name]()
            self.impending_change['enter_params'] = enter_params

    def pop(self):
        if self.current is not None:
            self.impending_change['current'] = self.states_stack.pop(-1)

    def update(self, dt):
        self.current.update(dt)

    def handle_events(self, events):
        self.current.handle_events(events)

    def render(self, render_screen):
        self.current.render(render_screen)

    def exit(self):
        self.should_exit = True
