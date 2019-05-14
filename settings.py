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

    def eval_line_list(self, line_list):
        key = line_list[0]
        values = line_list[1]

        if len(values) == 1:
            if values[0].startswith('$'):
                self.settings[key] = values[0][1:]
            else:
                self.settings[key] = int(values[0])
        else:
            command = ""
            for value in values:
                if value.startswith('$'):
                    command += f"self.settings['{value[1:]}']"
                else:
                    command += value
            self.settings[key] = eval(command)
