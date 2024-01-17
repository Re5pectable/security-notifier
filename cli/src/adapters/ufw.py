import subprocess
from typing import Literal

class UFW:
    
    active: bool
    profiles: dict[str: dict] = {}
    
    __command = ["sudo", "ufw", "status"]
    
    def __init__(self, output: str | None = None) -> None:
        if output is None:
            try:
                output = subprocess.check_output(self.__command).decode()
            except subprocess.CalledProcessError as e:
                raise ValueError(f'Cound not run {self.__command}')
        
        lowered_lines = output.lower().strip(' \n').split('\n')
        self.active = self._get_status(lowered_lines)
        if not self.active:
            return
        self.profiles = self._get_profiles(lowered_lines)
        
        
    def _get_status(self, lowered_lines: list[str]):
        for line in lowered_lines:
            if line.startswith('status:'):
                status = line.replace('status:', '').strip()
                if status == 'active':
                    return True
        return False


    def _get_profiles(self, lowered_lines: list[str]):
        for i, line in enumerate(lowered_lines):
            to_p = line.find('to')
            action_p = line.find('action')
            from_p = line.find('from')
            if all([action_p != -1, to_p != -1, from_p != -1]) and lowered_lines[i+1].count('-') > 5:
                values_row_index, columns_width = i+2, {'to': to_p, 'action': action_p, 'from': from_p}
                break
        else:
            raise ValueError('Columns are not found')
    
        values = {}
        for line in lowered_lines[values_row_index:]:
            to = line[columns_width['to']:columns_width['action']].strip()
            action = line[columns_width['action']:columns_width['from']].strip()
            from_ = line[columns_width['from']:].strip()
            values[to] = {'action': action, 'from': from_}
        return values
