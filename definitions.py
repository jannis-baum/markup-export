import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

from dotenv import load_dotenv
load_dotenv()

TEMPLATE_DIR = (lambda e: e if e else 'templates')(os.getenv('TEMPLATE_DIR'))
TEMPLATE_RECENT = (lambda e: e if e else '_recent')(os.getenv('TEMPLATE_RECENT'))

