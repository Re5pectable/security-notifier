import requests

_escape_chars = "\\.()[]*{}_>#-+|!~"

class Telegram:

    __url: str

    def __init__(self, token):
        self.__url = f"https://api.telegram.org/bot{token}/"

    def send_text(self, chat_id: int, text: str):
        for symbol in _escape_chars:
            text = text.replace(symbol, '\\' + symbol)
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "MarkdownV2"
        }
        response = requests.post(self.__url + 'sendMessage', data=payload)
        return response.status_code, response.json()
