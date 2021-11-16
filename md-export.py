#!/usr/bin/env python3

import os
from template_dir import TemplateDir

class MDExporter:
    def __init__(self):
        self.templates = TemplateDir(TemplateDir.template_path, '', 0)
    
    def templates_string(self):
        return TemplateDir.template_path + '\n' + self.templates.string()

if __name__ == '__main__':
    mde = MDExporter()
    print(mde.templates_string())

