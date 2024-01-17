from src.configuration import config_parser

SSH_PORT: int = config_parser.getint('Server', 'SSH_PORT')
TG_CHAT: int = config_parser.getint('Telegram', 'TG_CHAT')
WIREGUARD_SUBNET: str = config_parser.get('Server', 'WIREGUARD_SUBNET')