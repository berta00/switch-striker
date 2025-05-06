from src.core import manager

import threading
import time
import os
from scapy.all import sniff, wrpcap


# currently listening everyware
#core_interface = configuration.get_core_interface()

directory_path = os.path.dirname(os.path.realpath(__file__))

def run():

    sniff_thread = SniffThread()
    sniff_thread.daemon = True
    sniff_thread.start()

    return sniff_thread


class SniffThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            manager.sniffer_thread = 'on'
            while(manager.sniffer_thread == 'on'):
                sniffed_traffic = sniff(count=5)
                wrpcap(directory_path + '/../../pcap/intercepted.pcap', sniffed_traffic, append=True)

        except Exception as e:
            manager.sniffer_thread = f'error: {e}'
            return
        
        manager.sniffer_thread = 'off'

    def stop(self):
        if manager.sniffer_thread == 'on':
            return False
        elif manager.sniffer_thread[:5] == 'error':
            return False
        
        manager.sniffer_thread = 'off'
        self.join()

        return True 


