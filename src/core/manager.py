from src.cli import parser
from src.utilities import configuration
from src.web import server
from src.cli import menu
from src.attacks import mac_address_flooding

import time


web_server_thread = None

attacks_satus = 'off'
attack_type = ''

direct_attack = False


def run():

    manage_arguments()

    # running flask into a thread
    web_server_thread = server.run()
    time.sleep(1) # TODO: check when flask has printed shit

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
        mac_address_flooding.run()

    elif(choice[0] == 'Web interface Check status'):
        print(server.status())

    elif(choice[0] == f'Web interface Toggle (currently: {server.status()})'):
        if(server.status() == 'off'):
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

