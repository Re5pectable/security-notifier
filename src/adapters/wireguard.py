import subprocess


class Interface:
    name: str = None
    public_key: str = None
    listening_port: int = None


class Peer:
    public_key: str = None
    endpoint: str = None
    allowed_ips: str = None
    latest_handshake: str = None


class Wireguard:

    active: bool
    interaface: Interface = None
    peers: list[Peer] = []

    __comand = ["sudo", "wg"]

    def __init__(self, output: str | None = None) -> None:
        if output is None:
            try:
                output = subprocess.check_output(self.__comand).decode()
            except subprocess.CalledProcessError:
                raise ValueError(f'Cound not run {self.__comand}')
            
        output = output.strip(' \n') if output else ''
        
        if 'interface:' not in output:
            self.active = False
            return
        self.active = True
           
        lines = output.split('\n')
        
        interface_index = self.find_interface_entrace(lines)
        self.interaface = self.extract_interface(lines[interface_index:])
        
        peer_indexes = self.find_peer_entrace(lines)
        for index in peer_indexes:
            self.peers.append(self.extract_peer(lines[index:]))
            
        
    def find_interface_entrace(self, lines: list[str]) -> int:
        for i, line in enumerate(lines):
            if line.startswith('interface:'):
                return i
            
    def find_peer_entrace(self, lines: list[str]) -> list[int]:
        entrances = []
        for i, line in enumerate(lines):
            if line.startswith('peer:'):
                entrances.append(i)
        return entrances
    
    def extract_interface(self, lines: list[str]):
        if not lines[0].startswith('interface:'):
            raise ValueError('Interface not found')
        
        interface = Interface()
        interface.name = lines[0].replace('interface:', '').strip()
        
        for line in lines[1:]:
            if not line:
                break
            
            line_ = line.strip()
            if line_.startswith('public key:'):
                interface.public_key = line_.replace('public key:', '').strip()
                
            if line_.startswith('listening port:'):
                interface.listening_port = line_.replace('listening port:', '').strip()
            
        return interface
    
    def extract_peer(self, lines: list[str]):
        if not lines[0].startswith('peer:'):
            raise ValueError('Peer not found')
        
        peer = Peer()
        peer.public_key = lines[0].replace('peer:', '').strip()
        
        for line in lines[1:]:
            if not line:
                break
            
            line_ = line.strip()
            if line_.startswith('endpoint: '):
                peer.public_key = line_.replace('endpoint: ', '').strip()
                
            if line_.startswith('allowed ips: '):
                peer.allowed_ips = line_.replace('allowed ips: ', '').strip()
                
            if line_.startswith('latest handshake: '):
                peer.latest_handshake = line_.replace('latest handshake: ', '').strip()
        return peer
