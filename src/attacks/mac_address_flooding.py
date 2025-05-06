from src.core import manager
from src.cli import parser

import scapy

def run():
    manager.attacks_satus = 'running'
    manager.attack_type = 'mac_address_flooding'

    # aquire target
    target_address = parser.get_target_address()



def stop():
    manager.attacks_satus = 'off'
    manager.attack_type = ''

def status():
    if(manager.attack_status == 'running'):
        return 'Attack is running'
    if(manager.attack_status == 'error'):
        return 'Attack had an error'
