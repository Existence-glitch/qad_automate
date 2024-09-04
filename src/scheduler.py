import yaml
import time
import subprocess
import logging
import os
from datetime import datetime
from croniter import croniter

# Setup logging
log_dir = '/app/logs'
os.makedirs(log_dir, exist_ok=True)
scheduler_log = os.path.join(log_dir, 'scheduler.log')
executions_log = os.path.join(log_dir, 'executions.log')

logging.basicConfig(
    filename=scheduler_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add console handler for immediate feedback
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Setup execution logger
execution_logger = logging.getLogger('execution_logger')
execution_logger.setLevel(logging.INFO)
execution_handler = logging.FileHandler(executions_log)
execution_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
execution_logger.addHandler(execution_handler)

def load_executions(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading executions file: {str(e)}")
        return None

def run_command(command, task_name):
    logging.info(f"Attempting to run task: {task_name}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logging.info(f"Task '{task_name}' completed successfully")
        execution_logger.info(f"Task: {task_name}\nCommand: {command}\nOutput:\n{result.stdout}\n{'='*50}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Task '{task_name}' failed with error: {str(e)}")
        execution_logger.error(f"Task: {task_name}\nCommand: {command}\nError:\n{e.stderr}\n{'='*50}")
    except Exception as e:
        logging.error(f"Unexpected error running task '{task_name}': {str(e)}")
        execution_logger.error(f"Task: {task_name}\nCommand: {command}\nUnexpected Error:\n{str(e)}\n{'='*50}")
    return False

def setup_schedules(executions):
    schedules = []
    for execution in executions['executions']:
        cron = execution['schedule']
        command = execution['command']
        name = execution['name']
        try:
            cron_iter = croniter(cron, datetime.now())
            next_run = cron_iter.get_next(datetime)
            schedules.append({"cron": cron_iter, "command": command, "name": name, "next_run": next_run})
            logging.info(f"Scheduled: {name} - {cron} - Next run: {next_run}")
        except Exception as e:
            logging.error(f"Error setting up schedule for {name}: {str(e)}")
    return schedules

def run_scheduler():
    logging.info("Scheduler started")
    executions_file = '/app/config/programmed_executions.yaml'
    executions = load_executions(executions_file)
    if not executions:
        logging.error("Failed to load executions. Exiting.")
        return

    schedules = setup_schedules(executions)

    while True:
        now = datetime.now()
        for task in schedules:
            if task["next_run"] <= now:
                if run_command(task["command"], task["name"]):
                    # Only update next_run if the task was executed successfully
                    task["next_run"] = task["cron"].get_next(datetime)
                    logging.info(f"Next run for '{task['name']}': {task['next_run']}")
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_scheduler()