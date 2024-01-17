import json
from pathlib import Path

__PATH = Path(__file__).parent

logs_path = __PATH / 'logs.log'

_settings_path = __PATH / 'settings.json'
settings = json.load(open(_settings_path, 'r'))

WIREGUARD_PORT: int = settings['WIREGUARD_PORT']
SSH_PORT: int = settings['SSH_PORT']
WIREGUARD_SUBNETWORK: str = settings['WIREGUARD_SUBNETWORK']
TG_BOT_API: str = settings['TG_BOT_API']
TG_CHAT: int = settings['TG_CHAT']
