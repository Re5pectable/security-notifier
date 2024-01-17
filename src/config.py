import configparser
from pathlib import Path

DIRECTORY_PATH = Path(__file__).parent.parent

configuration = configparser.ConfigParser().read(DIRECTORY_PATH / 'config.ini')
