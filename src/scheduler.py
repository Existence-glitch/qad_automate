import yaml
import time
import subprocess
import logging
import os
from datetime import datetime
from croniter import croniter

# Setup logging
log_dir = '/app/logs'
log_file = os.path.join(log_dir, 'scheduler.log')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_executions(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def run_command(command, task_name):
    logging.info(f"Starting task: {task_name}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logging.info(f"Task '{task_name}' completed successfully")
        if result.stdout:
            logging.info(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Task '{task_name}' failed with error: {str(e)}")
        if e.stdout:
            logging.error(f"stdout: {e.stdout}")
        if e.stderr:
            logging.error(f"stderr: {e.stderr}")

def setup_schedules(executions):
    schedules = []
    for execution in executions['executions']:
        cron = execution['schedule']
        command = execution['command']
        name = execution['name']
        schedules.append((croniter(cron), command, name))
        logging.info(f"Scheduled: {name} - {cron}")
    return schedules

def main():
    logging.info("Scheduler started")
    executions_file = '/app/config/programmed_executions.yaml'
    executions = load_executions(executions_file)
    schedules = setup_schedules(executions)

    while True:
        now = datetime.now()
        for cron, command, name in schedules:
            if cron.get_next(datetime) <= now:
                run_command(command, name)
                cron.get_next()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()