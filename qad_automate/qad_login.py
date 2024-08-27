from utils import execute_commands, execute_command
from config import CONFIG
from commands import *

def login_qad(session, qad_version):
    if qad_version in CONFIG:
        if qad_version.startswith('new'):
            login_qad_new(session, qad_version)
        elif qad_version.startswith('old'):
            login_qad_old(session, qad_version)
    else:
        print(f"Invalid QAD version: {qad_version}")

def login_qad_new(session, config):
    execute_command(session, 'qadmenu', wait_for="Please Enter Your Selection:")
    execute_command(session, 'US', wait_for="User ID:")
    execute_command(session, config['user'], wait_for="Password:")
    execute_command(session, config['pass'])

def login_qad_old(session, config):
    execute_command(session, config['qadmenu'], wait_for="User Name")
    execute_command(session, config['username'], wait_for="Password")
    execute_command(session, config['password'], wait_for="QAD Menu")
    execute_command(session, '\n', wait_for="QAD Menu")  # Extra enter
    execute_command(session, ' ', wait_for="QAD Menu")  # Space to clear any messages

"""
def login_qad_new(session, qad_version):
    username = CONFIG[qad_version]['user']
    password = CONFIG[qad_version]['pass']

    login_commands = [
        'qadmenu',  # Enter qadmenu terminal
        enter(),
        'US',       # Select language
        enter()
    ]

    execute_commands(session, login_commands, 20)

def login_qad_old(session, qad_version):
    username = CONFIG[qad_version]['username']
    password = CONFIG[qad_version]['password']
    qadmenu = CONFIG[qad_version]['qadmenu']

    login_commands = [
        qadmenu,
        username,
        enter(),
        password,
        enter(),
        enter(),
        space(),
    ]

    execute_commands(session, login_commands, 1)

"""