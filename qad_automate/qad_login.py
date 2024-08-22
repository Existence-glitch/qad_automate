from utils import execute_commands
import os

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def login_qad(session):
    initial_commands = [
        '2',
        username,
        '\r',
        password,
        '\r',
        '\r',
        ' ',
    ]

    execute_commands(session, initial_commands)
