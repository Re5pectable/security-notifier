import os
from datetime import datetime

from src.adapters.telegram import Telegram

from .config import SERVER_NAME, TG_CHAT, TG_TOKEN

message_template = """
User *{username}* logged in to *{server_name}*

*{time}*
"""

def notify():
    user_ = os.getenv('USER')
    time_ = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
    server_name_ = SERVER_NAME
    
    text = message_template.format(
        username=user_,
        server_name=server_name_,
        time=time_
    )
    Telegram(TG_TOKEN).send_text(TG_CHAT, text)
