import paramiko
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
hostname = os.getenv('HOSTNAME')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def get_ssh_session():
    # Connect via ssh with credentials
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)

    # Open a session
    session = ssh_client.get_transport().open_session()
    session.get_pty(term='xterm')
    session.invoke_shell()
    return session

def send_command(session, command):
    # Execute command
    session.send(command)
    time.sleep(1)

    # Print session state
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output
