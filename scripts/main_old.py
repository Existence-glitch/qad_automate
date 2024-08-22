import os
import time
import paramiko

from dotenv import load_dotenv
from utils import strip_ansi
from config import *

def send_command_with_output(session, command):
    session.send(command)
    time.sleep(1)
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

# Send a command and press enter
def cmd_ent(session, command):
    session.send(command + '\r')
    time.sleep(1)
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

# Send a command without pressing enter
def cmd_snd(session, command):
    session.send(command)
    time.sleep(1)
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

# Send enter command
def ent(session):
    session.send('\r')
    time.sleep(1)
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

def spc(session):
    session.send(' ')
    time.sleep(1)
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

def get_ssh_session(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)
    session = ssh_client.get_transport().open_session()
    session.get_pty(term=TERMEMUL)
    session.invoke_shell()
    return session

def login_qad(username, password, s):
    # Select QAD PROD or PILO
    cmd_snd(s, QADENV)

    # Enter 'ID del Usuario'
    cmd_ent(s, username)

    # Enter 'Password'
    cmd_ent(s, password)

    # Enter 'Dominio' as SURFRUSD
    ent(s)

    # Pass to Menu Selection
    spc(s)
    print(spc(s))

def menu_qad(menu, s):
    a, b, c = menu.split('.')

    cmd_ent(s, a)
    cmd_ent(s, b)
    cmd_ent(s, c)

def main():
    # Load credentials from .env file
    load_dotenv()
    hostname = os.getenv('HOSTNAME')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Connect to server via ssh and get session 
    session = get_ssh_session(hostname, username, password)

    # Login to QAD
    login_qad(username, password, session)
    
    # Enter the desired menu
    menu_qad('36.2.13', session)

    # Execute the function assigned to given menu

    # Close session after
    session.close()
    paramiko.SSHClient().close()

if __name__ == '__main__':
    main()
