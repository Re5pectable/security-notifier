class NoAccessSituation(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__('Wireguard if off, but SSH available only from VPN', *args)
        
class SSHPortClosed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__('Cannot find opened SSH port', *args)
        
