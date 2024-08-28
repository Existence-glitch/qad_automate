import time

def enter():
    """
    Return the enter key character.
    """
    return '\r'

def space():
    """
    Return a space bar character.
    """
    return ' '

def wait_for_string(channel, expected_string, timeout=60):
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
            chunk = channel.recv(1024).decode('utf-8')
            buffer += chunk
            if expected_string in buffer:
                return True
        time.sleep(0.1)
    return False

def run_cmd(session, command, wait_for=None, timeout=60):
    """
    Execute a command after waiting for a specific string to appear in the output.
    
    :param session: Paramiko channel object
    :param command: Command to execute
    :param wait_for: String to wait for in the output before executing the command (optional)
    :param timeout: Maximum time to wait in seconds
    :return: Command output as a string
    """
    # Wait for the specified string before executing the command
    if wait_for:
        print(f"Waiting for string: {wait_for}")
        if not wait_for_string(session, wait_for, timeout):
            raise TimeoutError(f"Timed out waiting for '{wait_for}' before executing command '{command}'")
    
    # Send the command to the session
    print(f"Executing command: {command}")
    session.send(command)
    time.sleep(1) # Wait for the command to be processed

    # Capture all output until there's no more data
    output = session.recv(1024)
    while True:
        if session.recv_ready():
            chunk = session.recv(1024)
            output += chunk
            print(chunk, end="")  # Print each chunk to the terminal as it's received
        else:
            break
    
    # Ensure all data is printed
    print(output)
    return output

