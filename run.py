import sys

sys.dont_write_bytecode = True

from datetime import datetime

from adapters.telegram import Telegram
from adapters.ufw import UFW
from adapters.wireguard import Wireguard
from config import *

def report_ok(ufw: UFW, wg: Wireguard):
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
    
def report_emergency_ssh_on(ufw: UFW, wg: Wireguard):
    pass

def report_error(e: Exception):
    text = "`"
    text += "Got an error:\n" + str(e)
    text += "`"
    text += "\n——————————————————————————————\n"
    text += f"*#Error, {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}*"
    for symbol in "()#.":
        text = text.replace(symbol, '\\' + symbol)
    print(text)
    return Telegram.send_text(TG_CHAT, text)
    

def main():
    try:
        ufw = UFW()
        wg = Wireguard()
        report_ok(ufw, wg)
    except Exception as e:
        print(report_error(e))
    
    return
    
    
    if not ufw.active:
        print('UFW is not active')
        return
    
    wireguard_profile_key = f'{WIREGUARD_PORT}/udp'
    
    is_allowed_wireguard_port = ufw.profiles.get(wireguard_profile_key, {}).get('action') == 'allow'
    
    if is_allowed_wireguard_port and not wg.active:
        ssh_key = f'{SSH_PORT}/tcp'
        ufw.add_profile(ssh_key, 'allow')


if __name__ == '__main__':
    main()