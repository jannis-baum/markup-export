#!/usr/bin/env python3

from template_dir import TemplateDir
from mue_errors import *
import shutil
import os
import subprocess

class MUExporter:
    mue_dir = os.path.dirname(os.path.realpath(__file__))
    temporary_dir = os.path.join(mue_dir, 'temporary')
    temporary_template = 'template.yaml'

    cmd_editor = 'vim'

    def __init__(self):
        self.debug = False
        self.templates = TemplateDir(TemplateDir.template_dir, MUExporter.mue_dir, 0)

    def __run_cmd(self, args):
        out = None if self.debug else subprocess.DEVNULL
        cp = subprocess.run(args, stdout=out, stderr=out)
        if cp.returncode != 0:
            raise SubprocessFailed
    
    def templates_string(self):
        return TemplateDir.template_dir + '\n' + self.templates.string()

    def ready_template(self, path, edit):
        template_path = os.path.join(TemplateDir.template_dir, TemplateDir.template_recent)
        shutil.copy(path, template_path)
        if edit:
            self.__run_cmd([MUExporter.cmd_editor, template_path])


        # temporary template
        os.path.join(MUExporter.temporary_dir, MUExporter.temporary_template)

if __name__ == '__main__':
    mde = MUExporter()
    print(mde.templates_string())

