import shutil
import os
import subprocess
import yaml

from mue_template_data import MUETemplateData
from mue_errors import *

class MUExporter:
    mue_dir = os.path.dirname(os.path.realpath(__file__))
    temporary_dir = os.path.join(mue_dir, '.temporary')
    temporary_template = 'template.yaml'

    def __init__(self):
        self.debug = False
        self.templates = MUETemplateData(MUExporter.mue_dir)

    def templates_list_string(self):
        return self.templates.list_string()

    def ready_template(self, identifiable, edit):
        template_path = self.templates.path_for(identifiable)
        recent_path = os.path.join(MUETemplateData.template_dirname, MUETemplateData.template_recent)
        shutil.copy(template_path, recent_path)

        # if edit: edit(recent_path)

        template_data = self.templates.data_from(MUETemplateData.template_recent)

        # use and remove mue-config data

        temporary_path = os.path.join(MUExporter.temporary_dir, MUExporter.temporary_template)
        with open(temporary_path, 'w') as template_file:
            template_file.write('---\n')
            yaml.dump(template_data, template_file)
            template_file.write('...')

