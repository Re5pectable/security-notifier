import os
from datetime import datetime

from src.adapters.telegram import Telegram

from .config import SERVER_NAME, TG_CHAT, TG_TOKEN

message_template = """
User *{username}* logged in to *{server_name}*
{time}
"""

def notify():
    text = message_template.format(
        username=os.getenv('USER'),
        server_name=SERVER_NAME,
        time=datetime.now().strftime('%H:%M:%S %Y-%m-%d')
    )
    Telegram(TG_TOKEN).send_text(TG_CHAT, text)
