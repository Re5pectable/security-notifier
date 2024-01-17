import subprocess
from datetime import datetime

from src.adapters.telegram import Telegram

from .config import TG_CHAT, TG_TOKEN

template = """
*{time___}*——————————————————————————————

*UFW:*

`{ufw_output}`
—————————————————————————————————————————

*Wireguard:*

`{wg_output}`
——————————————————————————————————————————

*Who:*
`{who_output}`
—————————————————————————————————————————
"""

def get_ufw():
    return subprocess.check_output(['sudo', 'ufw', 'status', 'verbose']).decode().strip()

def get_wg():
    return subprocess.check_output(['sudo', 'wg']).decode().strip()

def get_who():
    return subprocess.check_output(['sudo', 'who']).decode().strip()

def main():
    text = template.format(
        time___=datetime.now().strftime('%H:%M:%S %Y-%m-%d'),
        ufw_output=get_ufw(),
        wg_output=get_wg(),
        who_output=get_who()
    )
    Telegram(TG_TOKEN).send_text(TG_CHAT, text)
    