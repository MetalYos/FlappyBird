from helpers import Singleton
import os


@Singleton
class Settings():
    def __init__(self):
        self.settings = {}

    def load(self, path):
        with open(path, 'r') as file:
            for line in file.readlines():
                if line.startswith('#') or line == '\n':
                    continue

                line_list = line.strip().replace(' ', '').split('=')
                line_list[1] = line_list[1].split(',')
                self.eval_line_list(line_list)

        self.settings['pipe_min_height'] = self.settings['ground_height'] + \
            self.settings['pipe_gap_min'] // 2
        self.settings['pipe_max_height'] = self.settings['window_height'] - \
            self.settings['pipe_gap_max'] - self.settings['pipe_min_height']

    def eval_line_list(self, line_list):
        key = line_list[0]
        values = line_list[1]

        if len(values) == 1:
            if values[0].startswith('$'):
                self.settings[key] = values[0][1:]
            else:
                self.settings[key] = int(values[0])
        else:
            result = 0
            l_value = 0
            if values[0].startswith('$'):
                l_value = self.settings[values[0][1:]]
            else:
                l_value = int(values[0])

            r_value = 0
            if values[2].startswith('$'):
                r_value = self.settings[values[2][1:]]
            else:
                r_value = int(values[2])

            if values[1] == '+':
                result = l_value + r_value
            if values[1] == '-':
                result = l_value - r_value
            if values[1] == '*':
                result = l_value * r_value
            if values[1] == '/':
                result = l_value / r_value
            if values[1] == '//':
                result = l_value // r_value
            if values[1] == '**':
                result = l_value ** r_value
            if values[1] == '%':
                result = l_value % r_value

            self.settings[key] = result
