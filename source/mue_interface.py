import argparse, re, sys, os

from source.muexporter import MUExporter
from source.mue_errors import *
from definitions import TEMPLATE_RECENT, QL_DEF

class MUEInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('file')
        self.parser.add_argument('-o', '--out', dest='out', metavar='filename', type=str, help='output filename')
        self.parser.add_argument('-t', '--template', dest='template', metavar='template', type=str, help='template identifier')
        # edit becomes None if -e without name, False if not given
        self.parser.add_argument('-e', '--edit', dest='edit', nargs='?', metavar='save_as', default=False, type=str, help='edit template before using, optionally save')
        self.parser.add_argument('-i', '--interactive', dest='interactive', action='store_true', help='be asked about all options interactively')
        self.parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='enable debug mode to receive pandoc stdout and stderr and prevent clearing of temporary files')
        self.parser.add_argument('-q', '--quicklook', dest='quicklook', action='store_true', help='use non-default quicklook behavior')

        self.exporter = MUExporter()
        options = self.__get_options()
        self.exporter.export(options)

    def __get_options(self):
        options = self.parser.parse_args()
        options.quicklook = not QL_DEF if options.quicklook else QL_DEF
        interactive = options.interactive; del options.interactive
        try:
            if not os.path.exists(options.file): raise FileNotFound
            if interactive:
                print('template\n' + self.exporter.templates_list_string())
                match = re.match(r'^(\S*)(( new)|( as new (\S*))?)?$', input('> '))
                if not match: raise InvalidPick
                options.template = match.group(1)
                if match.group(2): options.edit = None
                if match.group(5): options.edit = match.group(5) + '.yaml'
                return options
            if not options.template:
                options.template = TEMPLATE_RECENT
                return options
        except MUEError as e:
            self.parser.print_usage()
            print(e.message)
            sys.exit(1)
        except KeyboardInterrupt:
            print()
            sys.exit(0)
        
        return options

