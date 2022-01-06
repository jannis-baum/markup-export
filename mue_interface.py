import argparse, re, sys

from muexporter import MUExporter
from mue_template_data import MUETemplateData
from mue_errors import *

class MUEInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('file')
        self.parser.add_argument('-o', '--out', dest='out', metavar='filename', type=str, help='output filename')
        self.parser.add_argument('-t', '--template', dest='template', metavar='template', type=str, help='template identifier')
        # edit becomes None if -e without name, False if not given
        self.parser.add_argument('-e', '--edit', dest='edit', nargs='?', metavar='save_as', default=False, type=str, help='edit template before using, optionally save')
        self.parser.add_argument('-r', '--recent', dest='recent', action='store_true', help='use most recent template again')
        self.parser.add_argument('-i', '--interactive', dest='interactive', action='store_true', help='be asked about all options interactively')
        self.parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='enable debug mode to receive pandoc stdout and stderr and prevent clearing of temporary files')

        self.exporter = MUExporter()
        self.options = self.__get_options()
        self.__run()

    def __get_options(self):
        options = self.parser.parse_args()
        recent = options.recent; del options.recent
        interactive = options.interactive; del options.interactive
        try:
            if recent:
                if options.template or interactive: raise ExclusiveRecent
                options.template = MUETemplateData.template_recent
                return options
            if interactive:
                print('template\n' + self.exporter.templates_list_string())
                match = re.match(r'^(\S*)(( new)|( as new (\S*))?)?$', input('> '))
                if not match: raise InvalidPick
                options.template = match.group(1)
                if match.group(2): options.edit = None
                if match.group(5): options.edit = match.group(5) + '.yaml'
                return options
        except MUEError as e:
            self.parser.print_usage()
            print(e.message)
            sys.exit(1)

    def __run(self):
        print(self.options)

