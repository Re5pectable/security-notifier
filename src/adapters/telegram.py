import requests

from src.config import TG_BOT_API


class Telegram:
    bot_token = TG_BOT_API
    
    __base_url = f"https://api.telegram.org/bot{bot_token}/"
    
    @classmethod
    def send_text(cls, tg_id: int, text: str):
        for symbol in "()#./":
            text = text.replace(symbol, '\\' + symbol)
        payload = {
            "chat_id": tg_id,
            "text": text,
            "parse_mode": "MarkdownV2"
        }
        
        response = requests.post(cls.__base_url + 'sendMessage', data=payload)
        return response.status_code, response.json()
