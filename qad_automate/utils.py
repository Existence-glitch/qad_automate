import re
import time

# Function that escapes some undesired ANSI characters in the output
def strip_ansi(text):
    ansi_escape = re.compile(
        r'(?:\x1B[@-_]|[\x0e\x0f]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])'
    )
    return ansi_escape.sub('', text.decode('utf-8', 'ignore'))

def send_command(session, command):
    # Execute command
    session.send(command)
    time.sleep(1)

    # Print session state
    output = session.recv(1024)
    while session.recv_ready():
        output += session.recv(1024)
    return output

# Function that executes commands and shows processed output through the CLI
def execute_commands(session, commands):
    for command in commands:
        print(f"Executing: {command}")
        output = strip_ansi(send_command(session, command))
        print(output)
