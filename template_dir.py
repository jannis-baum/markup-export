import os

class TemplateDir:
    template_path = 'templates'

    def __init__(self, name, parent_path, depth):
        self.name = name
        self.path = os.path.join(parent_path, name)
        self.depth = depth
        self.entries = []
        self.__build()

    def __build(self):
        for entry in sorted(os.listdir(self.path)):
            if os.path.isdir(os.path.join(self.path, entry)):
                self.entries.append(TemplateDir(entry, self.path, self.depth + 1))
            elif entry[-5:] == '.yaml':
                self.entries.append(entry[:-5])
    
    def __string_lines(self):
        ret = []
        for i, entry in enumerate(self.entries):
            is_last = (i == len(self.entries) - 1)
            line = ' ' * self.depth * 4
            line += '└── ' if is_last else '├── '
            if type(entry) is TemplateDir:
                line += entry.name + '/'
                ret.append(line)
                inner_block = entry.__string_lines() if is_last else [
                    line[:self.depth * 4] + '│' + line[self.depth * 4 + 1:] for line in entry.__string_lines()
                ]
                ret += inner_block
            else:
                line += entry
                ret.append(line)
        return ret
    
    def string(self):
        return '\n'.join(self.__string_lines())
    
    def find(self, pattern):
        pass
        
