import paramiko
import time
import re

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname = 'qad.surfrut.com'
username = 'corellan'
password = 'corellan.,.'

ssh_client.connect(hostname=hostname, username=username, password=password)

# Set terminal type to xterm and establish session
session = ssh_client.get_transport().open_session()
session.get_pty(term='xterm')
session.invoke_shell()

def send_command(session, command):
    session.send(command)
    time.sleep(1)
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

def strip_ansi(text):
    ansi_escape = re.compile(
        r'(?:\x1B[@-_]|[\x0e\x0f]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])'
    )
    return ansi_escape.sub('', text.decode('utf-8', 'ignore'))

commands = [
    '2',
    'corellan',
    '\r',
    'corellan.,.',
    '\r',
    '\r',
    ' ',
    '36\r',
    '2\r',
    '13\r',
    'TEST SCRIPT PYTHON 1\r',
    'TEST SCRIPT PYTHON 1\r',
    '\r'
]

for command in commands:
    print(f"Executing: {command}")
    output = strip_ansi(send_command(session, command))
    print(output)

session.close()
ssh_client.close()
