from src.cli import parser
from src.utilities import configuration
from src.web import server
from src.cli import menu
from src.attacks import mac_address_flooding
from src.attacks import sniff
from src.core import manager

import time


web_server_thread = None
sniffer_thread = None
attack_thread = None

web_server_status = 'off'

sniffer_status = 'off'
attack_status = 'off'
attack_type = ''
snifed_packets = 0

direct_attack = False


def run():

    manage_arguments()

    manager.web_server_thread = server.run()

    menu.print_banner()
    while(True):
        manage_menu_choices(menu.run())


def manage_arguments():
    args = parser.parse()
    
    if(args.set_core_interface != None):
        configuration.set_core_interface(args.set_interface)
    
    if(args.set_web_server_port != None):
        configuration.get_web_server_port(args.set_port)

    if(args.launch_attack != None):
        direct_attack = True

        if(args.launch_attack == 'mac_address_flooding'):
            target = args.target_ip
            mac_address_flooding.run(target)


# TODO: better menu choice handling
def manage_menu_choices(choice):

    choice = choice.strip()
    choice = choice.split('||')

    if('←' in choice[0]):
        pass

    elif(choice[0] == 'Attack! Mac address flooding'):
        attack_thread = mac_address_flooding.run()

    elif(choice[0] == 'Attack! Sniffer'):
        sniff.run()

    elif(choice[0] == 'Attack! Stop attack'):
        if manager.attack_thread != None:
            manager.attack_thread.stop()

    elif(choice[0] == 'Attack! Stop sniffer'):
        if manager.sniffer_thread != None:
            manager.sniffer_thread.stop()

    elif(choice[0] == 'Web interface Check status'):
        print(web_server_status)

    elif(choice[0] == f'Web interface Toggle (currently: {manager.web_server_status})'):
        if(server.manager.web_server_status == 'off'):
            # creates new thread
            web_server_thread = server.run()
            print(web_server_thread)
        else:
            web_server_thread.stop()
    
    elif(choice[0] == f'Configuration Core interface'):
        configuration.set_core_interface(choice[1])
    
    elif(choice[0] == f'Configuration Web server port'):
        configuration.set_web_server_port(choice[1])
    
    elif(choice[0] == 'Exit'):
        exit()

