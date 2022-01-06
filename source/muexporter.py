import shutil
import os
import subprocess
import yaml

from source.templates.mue_template_data import MUETemplateData
from source.mue_errors import *
from definitions import ROOT_DIR

class MUExporter:
    temporary_dir = os.path.join(ROOT_DIR, MUETemplateData.template_temporary)
    temporary_template = 'template.yaml'

    def __init__(self):
        self.debug = False
        self.templates = MUETemplateData(ROOT_DIR)

    def templates_list_string(self):
        return self.templates.list_string()

    def ready_template(self, identifiable, edit):
        template_path = self.templates.path_for(identifiable)
        recent_path = os.path.join(MUETemplateData.template_dirname, MUETemplateData.template_recent)
        shutil.copy(template_path, recent_path)

        # if edit: edit(recent_path)

        config, template_data = self.templates.conf_and_template_from(MUETemplateData.template_recent)

        # use config data

        temporary_path = os.path.join(MUExporter.temporary_dir, MUExporter.temporary_template)
        with open(temporary_path, 'w') as template_file:
            template_file.write('---\n')
            yaml.dump(template_data, template_file)
            template_file.write('...')

