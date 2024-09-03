# QAD Automation Tool

## Overview

This project is an automation tool designed to interact with QAD systems via SSH. It supports both old and new versions of QAD, each with multiple environments. The tool allows users to log in to a specific QAD environment, navigate to a desired menu, and execute predefined functions within that menu.

## Project Structure

```
qad_automate/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── google-credentials.json
├── pyproject.toml
├── requirements.txt
├── setup.cfg
├── setup.py
├── config/
│   ├── config.yaml
│   ├── programmed_executions.yaml
├── docs/
│   ├── README.md
│   └── data/
├── logs/
├── scripts/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── qad_login.py
│   ├── qad_menus.py
│   ├── qad_ssh.py
│   ├── sheets.py
│   ├── utils.py
│   └── scheduler.py
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Existence-glitch/qad_automate.git
   cd qad-automate
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

### Manual Execution

Run the main script with the following command:

```
python src/main.py <qad_version> <menu_number> [function_index]
```

- `<qad_version>`: The version of QAD to connect to (e.g., 'new03', 'old01')
- `<menu_number>`: The menu number to navigate to (e.g., '61.3.16')
- `[function_index]`: (Optional) The index of the function to execute

If no function index is provided, the script will list available functions and prompt for user input.

### Scheduled Execution

The tool now supports cron-style scheduled executions. To set up scheduled tasks:

1. Edit the `programmed_executions.yaml` file in the `config` directory.
2. Add your desired scheduled tasks in the following format:

   ```yaml
   executions:
     - name: "Cron-style Task"
       command: "python /app/src/main.py <qad_version> <menu_number> <function_index>"
       schedule: "* * * * *"  # Cron schedule format
   ```

3. The scheduler will automatically pick up these tasks when the Docker container is started.

Note: The minimum interval for scheduled tasks is 1 minute. For cron-style schedules, you can specify the exact minute of execution.

## Docker

To run the application using Docker:

1. Build the Docker image:
   ```
   docker-compose build
   ```

2. Run the Docker container:
   ```
   docker-compose up -d
   ```

This will start the container with the scheduler running, which will execute the tasks defined in `programmed_executions.yaml`.

## Development

This project uses two branches:
- `main`: For stable releases
- `dev`: For development and testing

When pushing to these branches, GitHub Actions will automatically build and push Docker images to the GitHub Container Registry.

## Customization

- To add new menu functions, create a new Python file in the `menus` directory following the naming convention `menu_<menu_number>.py`.
- To modify scheduled tasks, edit the `programmed_executions.yaml` file.

## Troubleshooting

- Check the Docker logs for any error messages:
  ```
  docker-compose logs
  ```
- Ensure that the `config/programmed_executions.yaml` file is correctly formatted and mounted in the Docker container.
- Verify that the paths in the `programmed_executions.yaml` file are correct and point to the right locations within the Docker container.

## Contributing

Contributions to improve the tool or add new features are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## Author

- Name: Joaquín Tapia Riquelme
- Github: Existence-glitch

## License

[MIT License](LICENSE)