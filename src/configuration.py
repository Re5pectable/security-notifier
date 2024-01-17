import configparser
from pathlib import Path

DIRECTORY_PATH = Path(__file__).parent.parent

config_parser = configparser.ConfigParser()
config_parser.read(DIRECTORY_PATH / 'config.ini')
