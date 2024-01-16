class NoAccessSituation(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__('Wireguard if off, but SSH available only from VPN', *args)
