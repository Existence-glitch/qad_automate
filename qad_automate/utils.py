import re
import time
from config import get_env_config
from commands import *

# Function that escapes some undesired ANSI characters in the output
def strip_ansi(text):
    ansi_escape = re.compile(
        r'(?:\x1B[@-_]|[\x0e\x0f]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])'
    )
    return ansi_escape.sub('', text.decode('utf-8', 'ignore'))

def send_command(session, command, delay):
    # Execute command
    session.send(command)
    time.sleep(delay)

    # Print session state
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

# Function that executes commands and shows processed output through the CLI
def execute_commands(session, commands, delay):
    for command in commands:
        print(f"Executing: {command}")
        output = strip_ansi(send_command(session, command, delay))
        print(output)

def wait_for_string(channel, expected_string, timeout=30):
    """
    Wait for a specific string to appear in the channel output.
    
    :param channel: Paramiko channel object
    :param expected_string: String to wait for
    :param timeout: Maximum time to wait in seconds
    :return: True if the string was found, False if timeout occurred
    """
    start_time = time.time()
    buffer = ""
    while time.time() - start_time < timeout:
        if channel.recv_ready():
            chunk = channel.recv(1024).decode('utf-8', 'ignore')
            buffer += chunk
            if expected_string in buffer:
                return True
        time.sleep(0.1)
    return False

def execute_command(session, command, wait_for=None, timeout=50):
    """
    Execute a command and optionally wait for a specific string in the output.
    
    :param session: Paramiko channel object
    :param command: Command to execute
    :param wait_for: String to wait for in the output (optional)
    :param timeout: Maximum time to wait in seconds
    :return: Command output as a string
    """
    session.send(command + enter())
    if wait_for:
        if not wait_for_string(session, wait_for, timeout):
            raise TimeoutError(f"Timed out waiting for '{wait_for}' after command '{command}'")
    
    # Read the output
    output = ""
    while session.recv_ready():
        output += session.recv(1024).decode('utf-8', 'ignore')
    return output
