import dpkt
import json
import os


def main():
    print("Inserire quale funzione si vuole eseguire:")
    print("1. Leggere un file pcap")
    print("2. Inviare i dati a un template HTML")
    choice = input("Scelta (1/2): ")
    if choice == '1':
        path = input("Inserire il percorso del file pcap: ")
        read_pcap(path)
    elif choice == '2':
        path = input("Inserire il percorso del file pcap: ")
        send_data(path)


def read_pcap(path):
    with open(path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            #pacchetto letto come frame eth
            eth = dpkt.ethernet.Ethernet(buf)
            #stamp source e dest mac 
            #decodifica l'esadecimale in stringa con %02x per ogni byte
            
            print('Src MAC:', ':'.join('%02x' % b for b in eth.src))
            print('Dst MAC:', ':'.join('%02x' % b for b in eth.dst))
            
            
            
            #trasforma il pacchetto in bytes
            data = bytes(eth.data)
            #decodifica il pacchetto in base al protocollo
            text = data.decode('utf-8', errors='ignore')
            #stampa il contenuto del pacchetto
            print('Data:',text)
            print('-' * 30)
        

"""
{
    src: "sddd",
    dst: "sdad",
    data: "asdsadasd",
}

"""


def send_data(path):
    dati = []
    
    with open(path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            
            src = ':'.join('%02x' % b for b in eth.src)
            dst = ':'.join('%02x' % b for b in eth.dst)
            
            data = bytes(eth.data)
            text = data.decode('utf-8', errors='ignore')
            dati.append({"src": src, "dst": dst, "data": text})
            
    with open("src/utilities/pcap_reader/pcap.json", "w", encoding="utf-8") as file:
        json.dump(dati, file, ensure_ascii=False, indent=2)
                              
main()
