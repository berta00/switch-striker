import dpkt
import json
import os


def run(pcap_path='pcap/intercepted.pcap', result_path='pcap/readed.json'):
    dati = []
    
    with open(pcap_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            
            src = ':'.join('%02x' % b for b in eth.src)
            dst = ':'.join('%02x' % b for b in eth.dst)
            
            data = bytes(eth.data)
            text = data.decode('utf-8', errors='ignore')

            # json structure
            dati.append({"src": src, "dst": dst, "data": text})
            
    with open("pcap/readed.json", "w", encoding="utf-8") as file:
        json.dump(dati, file, ensure_ascii=False, indent=2)
                              
