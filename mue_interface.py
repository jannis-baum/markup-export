import argparse
from muexporter import MUExporter

class MUEInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('file')
        self.parser.add_argument('-o', '--out', dest='out', metavar='filename', type=str, help='output filename')
        self.parser.add_argument('-t', '--template', dest='template', metavar='template', type=str, help='template identifier')
        # edit becomes None if -e without name, False if not given
        self.parser.add_argument('-e', '--edit', dest='edit', nargs='?', metavar='save_as', default=False, type=str, help='edit template before using, optionally save')
        self.parser.add_argument('-r', '--recent', dest='recent', action='store_true', help='use most recent template again')
        self.parser.add_argument('-i', '--interaction', dest='interaction', action='store_true', help='be asked about all options interactively')
        self.parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='enable debug mode to receive pandoc stdout and stderr and prevent clearing of temporary files')

        self.exporter = MUExporter()
        self.__run()

    def __run(self):
        args = self.parser.parse_args()
        print(args)
