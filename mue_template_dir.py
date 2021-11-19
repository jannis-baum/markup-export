import os
import re

from mue_errors import *

class MUETemplateDir:
    def __init__(self, parent_path, name, depth=0):
        self.name = name
        self.depth = depth
        self.entries = []
        self.path = os.path.join(parent_path, self.name)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.__build()

    def __build(self):
        for entry in sorted(os.listdir(self.path)):
            if os.path.isdir(os.path.join(self.path, entry)):
                self.entries.append(MUETemplateDir(self.path, entry, self.depth + 1))
            elif entry[-5:] == '.yaml':
                self.entries.append(entry)
    
    def __string_lines(self):
        ret = []
        for i, entry in enumerate(self.entries):
            is_last = (i == len(self.entries) - 1)
            line = ' ' * self.depth * 4
            line += '└── ' if is_last else '├── '
            if type(entry) is MUETemplateDir:
                line += entry.name + '/'
                ret.append(line)
                inner_block = entry.__string_lines() if is_last else [
                    line[:self.depth * 4] + '│' + line[self.depth * 4 + 1:] for line in entry.__string_lines()
                ]
                ret += inner_block
            else:
                line += entry[:-5]
                ret.append(line)
        return ret
    
    def string(self):
        return '\n'.join(self.__string_lines())
    
    def find(self, pattern):
        p = pattern.split('/', 1)
        if len(p) > 1:
            for entry in self.entries:
                if type(entry) is MUETemplateDir and re.match(p[0], entry.name):
                    return entry.find(p[1])
        else:
            for entry in self.entries:
                if type(entry) is str and re.match(p[0], entry):
                    return os.path.join(self.path, entry)
        raise NoMatchFound
        
