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
        return self.templates.templates_list_string()

