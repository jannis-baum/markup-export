import yaml

from source.templates.mue_template_dir import MUETemplateDir
from definitions import TEMPLATE_DIR

class MUETemplateData:
    __key_include = 'include'
    __key_config = 'mue-config'
    template_temporary = 'template.yaml'

    def __init__(self, directory):
        self.t_dir = MUETemplateDir(directory, TEMPLATE_DIR)
    
    @staticmethod
    def __get_raw(path):
        with open(path, 'r') as template_file:
            return yaml.safe_load(template_file)

    @staticmethod
    def __include_data(inc, main):
        if type(main) != type(inc) or (type(main) is not dict and type(main) is not list):
            return main
        if type(main) is list:
            return list(dict.fromkeys(inc + main))
        d = inc.copy()
        for k in main:
            if k in d:
                d[k] = MUETemplateData.__include_data(d[k], main[k])
            else:
                d[k] = main[k]
        return d

    def list_string(self):
        return self.t_dir.string()

    def path_for(self, identifiable):
        return self.t_dir.find(identifiable)

    def conf_and_template_from(self, identifiable):
        data = MUETemplateData.__get_raw(self.path_for(identifiable))
        if not data:
            return dict(), dict()
        if MUETemplateData.__key_config not in data:
            return dict(), data

        included = list()
        while MUETemplateData.__key_include in data[MUETemplateData.__key_config]:
            if len(data[MUETemplateData.__key_config][MUETemplateData.__key_include]):
                inc_path = self.path_for(data[MUETemplateData.__key_config][MUETemplateData.__key_include].pop())
                if inc_path not in included:
                    included.append(inc_path)
                    data = MUETemplateData.__include_data(MUETemplateData.__get_raw(inc_path), data)
            else:
                data[MUETemplateData.__key_config].pop(MUETemplateData.__key_include)
        return data.pop(MUETemplateData.__key_config), data

