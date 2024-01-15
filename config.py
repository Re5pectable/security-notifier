import json

settings = json.load(open('./settings.json', 'r'))

WIREGUARD_PORT = settings['WIREGUARD_PORT']
WIREGUARD_IP_PREFIX = settings['WIREGUARD_IP_PREFIX']
SSH_PORT = settings['SSH_PORT']
TG_BOT_API = settings['TG_BOT_API']
TG_CHAT = settings['TG_CHAT']
