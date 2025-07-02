from src.core import manager
from src.utilities import pcap_reader

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
            manager.sniffer_status = 'on'
            while(manager.sniffer_status == 'on'):
                sniffed_traffic = sniff(count=1)
                wrpcap(directory_path + '/../../pcap/intercepted.pcap', sniffed_traffic) #TODO: possible logging option 
                pcap_reader.run()
                manager.snifed_packets += 1

        except Exception as e:
            manager.sniffer_status = f'error: {e}'
            manager.sniffer_thread = None
            return
        
        manager.sniffer_thread = None
        manager.sniffer_status = 'off'

    def stop(self):
        if manager.sniffer_thread != None:
            return False
        elif manager.sniffer_thread != None and manager.sniffer_status[:5] == 'error':
            return False
        
        manager.sniffer_thread = None
        manager.sniffer_status = 'off'
        self.join()

        return True 


