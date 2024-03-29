import shutil, os, sys
import subprocess, yaml

from script.templates.mue_template_data import MUETemplateData
from script.mue_errors import *
from definitions import ROOT_DIR, TEMPLATE_DIR, TEMPLATE_RECENT, CMD_EDITOR, CMD_QL

class MUExporter:
    __key_padoc_flags = 'pandoc-flags'
    temporary_dir = os.path.join(ROOT_DIR, '.temporary')
    temporary_templ_path = os.path.join(temporary_dir, MUETemplateData.template_temporary)

    def __init__(self):
        self.sp_output = subprocess.DEVNULL
        self.templates = MUETemplateData(ROOT_DIR)
    
    def __run_sp(self, cmds, shell=False):
        retc = subprocess.call(cmds, stdout=self.sp_output, stderr=self.sp_output, shell=shell)
        if retc != 0: raise SubprocessFailed

    def __safe_cp(self, src, dest):
        if not os.path.exists(dest) or not os.path.samefile(src, dest):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy(src, dest)

    def __ready_template_and_get_config(self, identifiable, edit):
        recent_path = os.path.join(TEMPLATE_DIR, TEMPLATE_RECENT)
        if identifiable:
            template_path = self.templates.path_for(identifiable)
            self.__safe_cp(template_path, recent_path)
        else:
            os.makedirs(os.path.dirname(recent_path), exist_ok=True)
            with open(recent_path, 'w'): pass

        if edit is not False:
            subprocess.call(CMD_EDITOR.format(recent_path), shell=True)
            if edit:
                save_path = os.path.join(TEMPLATE_DIR, edit)
                self.__safe_cp(recent_path, save_path)

        config, template_data = self.templates.conf_and_template_from(recent_path)
        with open(MUExporter.temporary_templ_path, 'w') as template_file:
            template_file.write('---\n')
            yaml.dump(template_data, template_file)
            template_file.write('...')
        
        return config

    def templates_list_string(self):
        return self.templates.list_string()

    def export(self, options):
        file_out = options.out or\
                ('.'.join(options.files[0].split('.')[:-1]) + '.pdf' if len(options.files) == 1\
                else 'export.pdf')
        self.sp_output = sys.stdout if options.debug else subprocess.DEVNULL

        config = self.__ready_template_and_get_config(options.template, options.edit)
        extra_flags = config[MUExporter.__key_padoc_flags] if MUExporter.__key_padoc_flags in config else []

        pandoc_args = ['pandoc'] + extra_flags + ['-s', '-o', file_out, MUExporter.temporary_templ_path]
        print(f'exporting {file_out} ...')
        self.__run_sp(pandoc_args
            + [f'--bibliography={bib}' for bib in options.bibs]
            + options.files
        )
        print('done')

        if options.quicklook:
            self.__run_sp(CMD_QL.format(file_out), shell=True)

