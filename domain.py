import subprocess
import sys
import traceback
from datetime import datetime

from adapters.logger import logger
from adapters.telegram import Telegram
from adapters.ufw import UFW
from adapters.wireguard import Wireguard
from config import *
from errors import NoAccessSituation

sys.dont_write_bytecode = True


def get_ufw_text(ufw: UFW):
    header = f"UFW active: {ufw.active}\n"
    rule_template = "  {action} {rule} {from_}"

    text = header
    text += "\n".join([
        rule_template.format(action=value['action'], rule=rule, from_=value['from'])
        for rule, value in ufw.profiles.items()
    ])
    return '`' + text + '`\n'


def get_wg_text(wg: Wireguard):
    header = f"Wireguard: {wg.active}\n"
    peer_template = "  {allowed_ips}, {latest_handshake}"

    text = header
    text += "\n".join([
        peer_template.format(allowed_ips=peer.allowed_ips, latest_handshake=peer.latest_handshake)
        for peer in wg.peers
    ])
    return '`' + text + '`\n'


def get_footer_text(error: Exception | None = None):
    devider = "——————————————————————————————"
    hashtag = '#Ok' if not error else f'#Error {str(error)}'
    time = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
    return f"{devider}\n*{hashtag}*, {time}"


def no_access_check(ufw: UFW, wg: Wireguard):
    ssh_ufw_settings = ufw.profiles.get(f'{SSH_PORT}/tcp', {})
    if all([
        not wg.active,
        ssh_ufw_settings.get('action') == 'allow',
        ssh_ufw_settings.get('from', '').startswith(WIREGUARD_IP_PREFIX)
    ]):
        raise NoAccessSituation()


def checks():
    ufw = UFW()
    logger.info('UFW created...')
    wg = Wireguard()
    logger.info('Wireguard created...')
    
    text = f"{get_wg_text(wg)}\n{get_ufw_text(ufw)}"

    try:
        no_access_check(ufw, wg)
        text += get_footer_text(error=None)
        
    except NoAccessSituation as e:
        logger.error('NoAccessSituation:', str(e))
        port_to_open = f'{SSH_PORT}/tcp'
        subprocess.run(['sudo', 'ufw', 'allow', port_to_open])
        subprocess.run(['sudo', 'systemctl', 'restart', 'ufw.service'])
        logger.error(f'Opened {port_to_open}')
        text += get_footer_text(error=e)
        
    except Exception as e:
        logger.error('Exception:', str(e))
        text += get_footer_text(error=e)
        
    finally:
        Telegram.send_text(TG_CHAT, text)


def main():
    logger.info('--- Start ---')
    try:
        checks()
    except Exception as e:
        logger.error(traceback.format_exc())
    logger.info('---- End ----')
