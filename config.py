import json
from pathlib import Path

__PATH = Path(__file__).parent

logs_path = __PATH / 'logs.log'

_settings_path = __PATH / 'settings.json'
settings = json.load(open(_settings_path, 'r'))

WIREGUARD_PORT = settings['WIREGUARD_PORT']
WIREGUARD_IP_PREFIX = settings['WIREGUARD_IP_PREFIX']
SSH_PORT = settings['SSH_PORT']
TG_BOT_API = settings['TG_BOT_API']
TG_CHAT = settings['TG_CHAT']
