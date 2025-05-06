from src.core import manager
from src.attacks import mac_address_flooding
from src.web import server

import os
import questionary


def run():
    
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
    f'\nSniffer: {manager.sniffer_thread}\n\nCurrently: {manager.attack_status}\nAttack type: {manager.attack_type}\n\nAttack menu: ',
        choices=[
            'Mac address flooding',
            'Coming soon',
            '←'
        ]
    ).ask()
        
    return choice

def print_web_interface_menu():
    choice = questionary.select(
    '\nWeb interface menu: ',
        choices=[
            'Check status',
            f'Toggle (currently: {server.status()})',
            '←'
        ]
    ).ask()
        
    return choice

def print_configuration_menu():
    choice = questionary.select(
    '\nConfiguration menu: ',
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
              _ _       _               _        _ _             
 _____      _(_) |_ ___| |__        ___| |_ _ __(_) | _____ _ __ 
/ __\ \ /\ / / | __/ __| '_ \ _____/ __| __| '__| | |/ / _ \ '__|
\__ \\ V  V /| | || (__| | | |_____\__ \ |_| |  | |   <  __/ |   
|___/ \_/\_/ |_|\__\___|_| |_|     |___/\__|_|  |_|_|\_\___|_|   
    
'''
    )

