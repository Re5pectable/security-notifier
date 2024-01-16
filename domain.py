import sys

sys.dont_write_bytecode = True

import logging
from datetime import datetime

from adapters.telegram import Telegram
from adapters.ufw import UFW
from adapters.wireguard import Wireguard
from config import *

logger = logging.getLogger(__name__)

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO) 

file_handler = logging.FileHandler('./logs.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def report(ufw: UFW, wg: Wireguard):
    text = "`"
    text += f"Wireguard: {wg.active}\n"
    text += "\n".join([f"  {peer.allowed_ips}, {peer.latest_handshake}" for peer in wg.peers]) + '\n\n'
    text += "UFW rules:\n"
    text += "\n".join([f"  {value['action']} {rule} {value['from']}" for rule, value in ufw.profiles.items()])
    text += "`"
    text += "\n——————————————————————————————\n"
    text += f"*#OK, {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}*"
    for symbol in "()#.":
        text = text.replace(symbol, '\\' + symbol)
    return Telegram.send_text(TG_CHAT, text)

def report_error(e: Exception):
    text = "`"
    text += "Got an error:\n" + str(e)
    text += "`"
    text += "\n——————————————————————————————\n"
    text += f"*#Error, {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}*"
    for symbol in "()#.":
        text = text.replace(symbol, '\\' + symbol)
    return Telegram.send_text(TG_CHAT, text)

def emergency_ssh_open(ufw: UFW, wg: Wireguard):
    ssh_ufw_settings = ufw.profiles.get(f'{SSH_PORT}/tcp', {}) 
    logger.info(ssh_ufw_settings)
    if all([
        not wg.active,
        ssh_ufw_settings.get('action') == 'allow',
        ssh_ufw_settings.get('from', f'{SSH_PORT}/tcp').startswith(WIREGUARD_IP_PREFIX)
    ]):
        ufw.add_profile('allow', )
        return Telegram.send_text(TG_CHAT, f'🔴🔴🔴🔴🔴 Turning on {SSH_PORT}')        
    

def main():
    try:
        logger.info('Start')
        ufw = UFW()
        wg = Wireguard()
        emergency_ssh_open(ufw, wg)
        status, _ = report(ufw, wg)
        logger.info('Success, ' + str(status))
    except Exception as e:
        logger.info('Error: ' +  str(e))
        print(report_error(e))
    
    return
