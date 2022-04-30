import argparse, re, sys, os

from script.muexporter import MUExporter
from script.mue_errors import *
from definitions import TEMPLATE_RECENT, QL_DEF

class MUEInterface:
    def __init__(self):
        self.exporter = MUExporter()

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('sources', nargs='+', type=str, help='source file(s) and / or directory/ies')
        self.parser.add_argument('-o', '--out', dest='out', metavar='filename', type=str, help='output filename')
        self.parser.add_argument('-t', '--template', dest='template', metavar='template', type=str, help='template identifier')
        # edit becomes None if -e without name, False if not given
        self.parser.add_argument('-e', '--edit', dest='edit', nargs='?', metavar='save_as', default=False, type=str, help='edit template before using, optionally save')
        self.parser.add_argument('-i', '--interactive', dest='interactive', action='store_true', help='be asked about all options interactively')
        self.parser.add_argument('-r', '--recent', dest='recent', action='store_true', help='use most recent template again')
        self.parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='enable debug mode to receive pandoc stdout and stderr and prevent clearing of temporary files')
        self.parser.add_argument('-q', '--quicklook', dest='quicklook', action='store_true', help='use non-default quicklook behavior')

        options = self.__get_options()

        try:
            self.exporter.export(options)
        except MUEError as e:
            self.__terminal_error(e)
        except KeyboardInterrupt:
            print()
            sys.exit(0)

    def __get_options(self):
        options = self.parser.parse_args()
        options.quicklook = not QL_DEF if options.quicklook else QL_DEF
        if options.edit: options.edit += '.yaml'

        recent = options.recent; del options.recent
        interactive = options.interactive; del options.interactive
        try:
            options.files = []; options.bibs = []
            for source in options.sources:
                if os.path.isdir(source):
                    files = [os.path.join(root, file) for root, _, files in os.walk(source) for file in files]
                elif os.path.isfile(source):
                    files = [source]
                else:
                    raise FileNotFound
                options.files += [file for file in files if file.endswith('md')]
                options.bibs += [file for file in files if file.endswith(('bib', 'bibtex', 'json', 'yaml', 'ris'))]
            del options.sources
            if len(options.files) == 0: raise NoFiles
            if recent:
                if options.template or interactive: raise ExclusiveRecent
                options.template = TEMPLATE_RECENT
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
            self.__terminal_error(e)
        except KeyboardInterrupt:
            print()
            sys.exit(0)
        
        return options

    def __terminal_error(self, e):
        print(e.message, end='\n\n')
        self.parser.print_usage()
        sys.exit(1)

