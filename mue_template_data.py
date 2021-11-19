import yaml

from mue_template_dir import MUETemplateDir

class MUETemplateData:
    __key_include = 'mue-include '
    template_dirname = 'templates'
    template_recent = '_recent.yaml'

    @staticmethod
    def __merge_lists(lists):
        ret = set()
        for l in lists:
            if type(l) is list:
                ret.update(MUETemplateData.__merge_lists(l))
            else: ret.add(l)
        return list(ret)

    @staticmethod
    def __data_to_kv(data):
        if type(data) is dict: return data.items()
        elif type(data) is list: return zip(range(len(data)), data)
        else: return zip([0], [data])

    @staticmethod
    def __data_at_key_stack(data, key_stack):
        d = data.copy()
        for key in key_stack:
            d = dict(MUETemplateData.__data_to_kv(d))
            if key in d: d = d[key]
            else: return dict()
        return d

    def __init__(self, directory):
        self.t_dir = MUETemplateDir(directory, MUETemplateData.template_dirname)
    
    def __get_raw(self, identifiable):
        path = self.path_for(identifiable)
        with open(path, 'r') as template_file:
            return path, yaml.safe_load(template_file)

    def __process_includes(self, data, key_stack=[], included=[]):
        includes = list()
        delete_keys = list()
        for key, value in MUETemplateData.__data_to_kv(data):
            if type(value) in [list, dict]:
                data[key] = self.__process_includes(value, key_stack + [key], included)
            elif value.startswith(MUETemplateData.__key_include):
                delete_keys.append(key)
                includes.append(value.split(' ', 1)[1])
        if includes:
            for dk in delete_keys: data.pop(dk)
            merge = list()
            for inc in includes:
                path, raw = self.__get_raw(inc)
                if path not in included:
                    included.append(path)
                    merge.append(self.__data_at_key_stack(raw, key_stack))
            return MUETemplateData.__merge_lists(merge + [data])
        return data
    
    def path_for(self, identifiable):
        return self.t_dir.find(identifiable)

    def data_from(self, identifiable):
        path, raw = self.__get_raw(identifiable)
        return self.__process_includes(raw, included=[path])

    def list_string(self):
        return MUETemplateData.template_dirname + '\n' + self.t_dir.string()

