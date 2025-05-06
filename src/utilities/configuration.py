import toml
import os

directory_path = os.path.dirname(os.path.realpath(__file__))

configuration = toml.load(directory_path + '/../../config/global.toml')

def write_changes():
    with open(directory_path + '/../../config/global.toml', 'w') as configuration_new:
        toml.dump(configuration, configuration_new)


def set_core_interface(interface):
    configuration['core']['interface'] = interface
    write_changes()

def get_core_interface():
    return configuration['core']['interface']


def set_web_server_port(port):
    configuration['web_server']['port'] = port
    write_changes()

def get_web_server_port():
    return configuration['web_server']['port']
