from src.core import manager
from src.attacks import mac_address_flooding
from src.web import server

import os
import questionary


def run():
    
    if(manager.attacks_satus != 'off'):
        if(manager.attack_type == 'mac_address_flooding'):
            print(mac_address_flooding.status())
    
    final_choice = print_menu()
    choice = ''

    if final_choice == 'Attack!':
        choice = print_attack_menu()

    elif final_choice == 'Web interface':
        choice = print_web_interface_menu()

    elif final_choice == 'Configuration':
        choice = print_configuration_menu()

    final_choice += ' ' + choice
    return final_choice


def clear():
    os.system('clear')

def print_menu():
    choice = questionary.select(
        "\nMenu:",
        choices=[
            'Attack!',
            'Web interface',
            'Configuration',
            'Exit'
        ]
    ).ask()

    return choice

def print_attack_menu():
    choice = questionary.select(
    'Attack menu: ',
        choices=[
            'Mac address flooding',
            'Coming soon',
            '←'
        ]
    ).ask()
        
    return choice

def print_web_interface_menu():
    choice = questionary.select(
    'Web interface menu: ',
        choices=[
            'Check status',
            f'Toggle (currently: {server.status()})',
            '←'
        ]
    ).ask()
        
    return choice

def print_configuration_menu():
    choice = questionary.select(
    'Configuration menu: ',
        choices=[
            'Core interface',
            'Web server port',
            '←'
        ]
    ).ask()

    if('←' not in choice):
        choice_value = questionary.text(f'Input {choice.lower()}:').ask()
        choice += f'||{choice_value}'
        
    return choice

def print_banner():
    clear()
    print(
'''
██╗     ██████╗       ███████╗██╗   ██╗██╗████████╗███████╗
██║     ╚════██╗      ██╔════╝██║   ██║██║╚══██╔══╝██╔════╝
██║      █████╔╝█████╗███████╗██║   ██║██║   ██║   █████╗  
██║     ██╔═══╝ ╚════╝╚════██║██║   ██║██║   ██║   ██╔══╝  
███████╗███████╗      ███████║╚██████╔╝██║   ██║   ███████╗
╚══════╝╚══════╝      ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝
'''
    )

