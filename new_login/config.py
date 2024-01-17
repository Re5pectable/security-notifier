from src.configuration import config_parser

SSH_PORT: int = config_parser.getint('Server', 'SSH_PORT')
SERVER_NAME: str = config_parser.get('Server', 'NAME')
TG_TOKEN: str = config_parser.get('Telegram', 'TOKEN')
TG_CHAT: int = config_parser.getint('Telegram', 'CHAT_ID')
