import shutil
import os
import subprocess
import yaml

from mue_template_dir import MUETemplateDir
from mue_errors import *

class MUExporter:
    mue_dir = os.path.dirname(os.path.realpath(__file__))
    temporary_dir = os.path.join(mue_dir, '.temporary')
    temporary_template = 'template.yaml'

    def __init__(self):
        self.debug = False
        self.templates = MUETemplateDir(MUETemplateDir.template_dir, MUExporter.mue_dir, 0)

    def __get_template_data(self, identifiable):
        with open(self.templates.find(identifiable), 'r') as template_file:
            # wip:
            # - recursively merge included files
            # - retrieve other mue-config and use it, remove it from return
            return yaml.safe_load(template_file)
    
    def templates_string(self):
        return MUETemplateDir.template_dir + '\n' + self.templates.string()

    def ready_template(self, identifiable, edit):
        template_path = self.templates.find(identifiable)
        recent_path = os.path.join(MUETemplateDir.template_dir, MUETemplateDir.template_recent)
        
        shutil.copy(template_path, recent_path)
        if edit: edit(recent_path)

        template_data = self.__get_template_data(identifiable)

        temporary_path = os.path.join(MUExporter.temporary_dir, MUExporter.temporary_template)
        with open(temporary_path, 'w') as template_file:
            template_file.write('---\n')
            yaml.dump(template_data, template_file)
            template_file.write('...')

