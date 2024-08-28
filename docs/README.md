# QAD Automation Tool

## Overview

This project is an automation tool designed to interact with QAD systems via SSH. It supports both old and new versions of QAD, each with multiple environments. The tool allows users to log in to a specific QAD environment, navigate to a desired menu, and execute predefined functions within that menu.

## Project Structure

The project consists of several Python files, each responsible for different aspects of the automation:

1. `main.py`: The entry point of the application. It handles command-line arguments and orchestrates the overall flow of the program.
2. `qad_ssh.py`: Manages SSH connections to the QAD environments.
3. `qad_login.py`: Handles the login process for different QAD versions.
4. `qad_menus.py`: Contains logic for navigating menus and executing menu-specific functions.
5. `utils.py`: Provides utility functions used throughout the project.
6. `config.py`: Manages configuration settings for different QAD environments.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/qad-automation-tool.git
   cd qad-automation-tool
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root directory and define the environment variables used in the `config.yaml` file:

```
NEW01_HOSTNAME=hostname1
NEW01_USERNAME=username1
NEW01_PASSWORD=password1
NEW01_USER=user1
NEW01_PASS=pass1

# Repeat for NEW02, NEW03, OLD01, and OLD02
```

## Usage

To run the automation tool, use the following command:

```
python main.py <qad_version> <menu_number>
```

- `<qad_version>`: Specifies the QAD version and environment (e.g., new01, old02)
- `<menu_number>`: The menu you want to navigate to (e.g., 36.6.13)

Example:
```
python main.py new01 36.6.13
```

This command will:
1. Connect to the QAD environment specified by `new01`
2. Log in to the system
3. Navigate to menu 36.6.13
4. Display available functions for this menu
5. Prompt the user to choose a function to execute

## Adding New Menu Functions

To add new menu functions, edit the `menu_navigation.py` file:

1. For new QAD versions, add entries to the `menu_functions_new` dictionary.
2. For old QAD versions, add entries to the `menu_functions_old` dictionary.

Example:
```python
menu_functions_new = {
    "36.6.13": {
        "function1_new": lambda session: run_cmd(session, "new_command1" + enter()),
        "function2_new": lambda session: run_cmd(session, "new_command2" + enter()),
    },
    "42.7.1": {
        "print_report": lambda session: run_cmd(session, "print_report" + enter()),
        "export_data": lambda session: run_cmd(session, "export_data" + enter()),
    },
}

menu_functions_old = {
    "36.6.13": {
        "function1_old": lambda session: run_cmd(session, "old_command1" + enter()),
        "function2_old": lambda session: run_cmd(session, "old_command2" + enter()),
    },
}
```

## Error Handling

The tool includes basic error handling:
- It will display an error message if the required command-line arguments are not provided.
- SSH connection errors and login failures will be reported to the user.
- If a specified menu or function is not found, an appropriate message will be displayed.

## Limitations

- The tool currently supports only predefined menu functions. Custom command execution is not supported.
- It assumes that the menu structure remains consistent. Any changes in the QAD system's menu structure may require updates to the navigation logic.

## Contributing

Contributions to improve the tool or add new features are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## Author

Name: Joaquín Tapia Riquelme
Github: Existence-glitch