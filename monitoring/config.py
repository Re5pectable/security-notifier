from src.configuration import config_parser

SERVER_NAME: str = config_parser.get('Server', 'NAME')
TG_TOKEN: str = config_parser.get('Telegram', 'TOKEN')
TG_CHAT: int = config_parser.getint('Telegram', 'MONITORING_CHAT_ID')

if not all([
    SERVER_NAME,
    TG_TOKEN,
    TG_CHAT
]):
    raise ValueError('Cannot extract configuration')
