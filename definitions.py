import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

from dotenv import load_dotenv
load_dotenv()

CMD_EDITOR = os.getenv('CMD_EDITOR', 'vim')
CMD_QL = os.getenv('CMD_QUICKLOOK', 'open')

QL_DEF = os.getenv('QUICKLOOK_BY_DEFAULT', False) in ['true', 1, 't', 'True', 'T']

TEMPLATE_DIR = os.getenv('TEMPLATE_DIR', 'templates')
TEMPLATE_RECENT = os.getenv('TEMPLATE_RECENT', '_recent')

