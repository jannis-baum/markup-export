import shutil, os, sys
import subprocess, yaml

from source.templates.mue_template_data import MUETemplateData
from source.mue_errors import *
from definitions import ROOT_DIR, TEMPLATE_DIR, TEMPLATE_RECENT, CMD_EDITOR, CMD_QL

class MUExporter:
    temporary_dir = os.path.join(ROOT_DIR, '.temporary')

    def __init__(self):
        self.sp_output = subprocess.DEVNULL
        self.templates = MUETemplateData(ROOT_DIR)

    def __ready_template_and_get_config(self, identifiable, edit):
        recent_path = os.path.join(TEMPLATE_DIR, TEMPLATE_RECENT)
        if identifiable:
            template_path = self.templates.path_for(identifiable)
            shutil.copy(template_path, recent_path)
        else:
            with open(recent_path, 'w'): pass

        # if edit not False: edit(recent_path)
        # if edit: save recent_path as edit

        config, template_data = self.templates.conf_and_template_from(TEMPLATE_RECENT)
        temporary_path = os.path.join(MUExporter.temporary_dir, MUETemplateData.template_temporary)
        with open(temporary_path, 'w') as template_file:
            template_file.write('---\n')
            yaml.dump(template_data, template_file)
            template_file.write('...')
        
        return config

    def templates_list_string(self):
        return self.templates.list_string()

    def export(self, options):
        print(options)
        self.sp_output = sys.stdout if options.debug else subprocess.DEVNULL
        config = self.__ready_template_and_get_config(options.template, options.edit)
        print(config)

