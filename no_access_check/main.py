import subprocess
import traceback
from datetime import datetime

from src.adapters.logger import logger
from src.adapters.telegram import Telegram
from src.adapters.ufw import UFW
from src.adapters.wireguard import Wireguard
from src.config import *
from src.utils.errors import NoAccessSituation, SSHPortClosed


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
    header = f"Wireguard active: {wg.active}\n"
    peer_template = "  {allowed_ips}, {latest_handshake}"

    text = header
    text += "\n".join([
        peer_template.format(allowed_ips=peer.allowed_ips, latest_handshake=peer.latest_handshake)
        for peer in wg.peers
    ])
    return '`' + text + '`\n'


def get_footer_text(errors: list[Exception]):
    devider = "——————————————————————————————"
    hashtag = '#Ok' if not errors else f"#Error [{', '.join([type(error).__name__ for error in errors])}]"
    time = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
    return f"{devider}\n*{hashtag}*, {time}"


def ssh_open_check(ufw: UFW, wg: Wireguard):
    ssh_ufw_settings = ufw.profiles.get(f'{SSH_PORT}/tcp')
    if not ssh_ufw_settings:
        raise SSHPortClosed()

def no_access_check(ufw: UFW, wg: Wireguard):
    ssh_ufw_settings = ufw.profiles.get(f'{SSH_PORT}/tcp')
    if all([
        not wg.active,
        ssh_ufw_settings.get('action') == 'allow',
        ssh_ufw_settings.get('from') == WIREGUARD_SUBNETWORK
    ]):
        raise NoAccessSituation()


def checks():
    ufw = UFW()
    logger.info('UFW created...')
    wg = Wireguard()
    logger.info('Wireguard created...')
    
    errors = []
    text = f"{get_wg_text(wg)}\n{get_ufw_text(ufw)}"
    
    try:
        ssh_open_check(ufw, wg)
    except SSHPortClosed as e:
        logger.error(type(e).__name__, str(e))
        port_to_open = f'{SSH_PORT}/tcp'
        subprocess.run(['sudo', 'ufw', 'allow', 'from', WIREGUARD_SUBNETWORK, 'to', 'any', 'port', str(SSH_PORT), 'proto', 'tcp'])
        subprocess.run(['sudo', 'systemctl', 'restart', 'ufw.service'])
        logger.error(f'Opened {port_to_open} to 10.0.0.0/24')
        errors.append(e)
        ufw = UFW()

    try:
        no_access_check(ufw, wg)
    except NoAccessSituation as e:
        logger.error(type(e).__name__, str(e))
        port_to_open = f'{SSH_PORT}/tcp'
        subprocess.run(['sudo', 'ufw', 'allow', port_to_open])
        subprocess.run(['sudo', 'systemctl', 'restart', 'ufw.service'])
        logger.error(f'Opened {port_to_open} to everyone')
        errors.append(e)
        ufw = UFW()
    
    text += get_footer_text(errors)
    
    Telegram.send_text(TG_CHAT, text)


def main():
    pass
    # logger.info('--- Start ---')
    # try:
    #     checks()
    # except Exception as e:
    #     logger.error(traceback.format_exc())
    # logger.info('---- End ----')
