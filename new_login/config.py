from src.configuration import config_parser

telegram_token = config_parser.get('Telegram', 'BOT_TOKEN')
telegram_chat_id = config_parser.get('Telegram', 'CHAT_ID')
server_name = config_parser.get('Server', 'NAME')
