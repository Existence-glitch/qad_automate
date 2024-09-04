import re
import time

def enter():
    """
    Return the enter key character.
    """
    return '\r'

def enter_n(n):
    """
    Return the enter key character n times.
    """
    return '\r' * n

def space():
    """
    Return a space bar character.
    """
    return ' '

def enterF4():
    """
    Return the F4 key.
    """
    return '\x1bOS'

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

def clean_ansi_escape_sequences(text):
    """
    Remove ANSI escape sequences and control characters from the text.
    
    :param text: Input text
    :return: Cleaned text
    """
    # Remove ANSI escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text = ansi_escape.sub('', text)
    
    # Remove other control characters except newline and carriage return
    text = ''.join(ch for ch in text if ord(ch) >= 32 or ch in '\n\r')
    
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    
    return text

def run_cmd(session, command, wait_for=None, timeout=60, debug=False):
    """
    Execute a command after waiting for a specific string to appear in the output.

    :param session: Paramiko channel object
    :param command: Command to execute
    :param wait_for: String to wait for in the output before executing the command (optional)
    :param timeout: Maximum time to wait in seconds
    :param debug: If True, print full output; if False, only print command execution message (default False)
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
    time.sleep(1)  # Wait for the command to be processed

    # Capture all output until there's no more data
    output = b""
    cleaned_output = ""
    while True:
        if session.recv_ready():
            chunk = session.recv(1024)
            output += chunk
            # Clean and print each chunk as it's received
            cleaned_chunk = clean_ansi_escape_sequences(chunk.decode('utf-8', errors='ignore'))
            cleaned_output += cleaned_chunk
            if debug:
                print(cleaned_chunk, end="")
        else:
            # Check if there's more data after a short delay
            time.sleep(0.1)
            if not session.recv_ready():
                break

    # Remove empty lines from the final cleaned output
    cleaned_output = '\n'.join(line for line in cleaned_output.splitlines() if line.strip())

    return cleaned_output

def capture_output(session, start_string, end_string, append_string):
    """
    Capture output between two strings and append another string.

    :param session: Paramiko channel object
    :param start_string: String to start capturing output after
    :param end_string: String to stop capturing output before
    :param append_string: String to append to the captured output
    :return: Captured output with the appended string
    """
    output = run_cmd(session, space())
    start_index = output.find(start_string) + len(start_string)
    end_index = output.find(end_string)
    captured_output = output[start_index:end_index]
    return captured_output + append_string
