import argparse


parser = argparse.ArgumentParser(
    prog='raspi-L2',
    description='TODO',
    epilog='TODO'
)


# DIRECT ATTACK
# launch attack
parser.add_argument('-la', '--launch-attack')
# target ip
parser.add_argument('-ti', '--target-ip')


# SETTINGS
# change core interface
parser.add_argument('-si', '--set-core-interface')
# change web server port
parser.add_argument('-sp', '--set-web-server-port')


def parse():
    arguments = parser.parse_args()

    # arguments dependency
    if arguments.launch_attack != None and arguments.target_ip == None:
        parser.print_help()
        exit(-1)
    
    return arguments
