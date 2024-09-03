import yaml
import time
import subprocess
from datetime import datetime
from croniter import croniter

def load_executions(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def run_command(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)

def setup_schedules(executions):
    schedules = []
    for execution in executions['executions']:
        cron = execution['schedule']
        command = execution['command']
        schedules.append((croniter(cron), command))
        print(f"Scheduled: {execution['name']} - {cron}")
    return schedules

def main():
    executions_file = '/app/config/programmed_executions.yaml'
    executions = load_executions(executions_file)
    schedules = setup_schedules(executions)

    while True:
        now = datetime.now()
        for cron, command in schedules:
            if cron.get_next(datetime) <= now:
                run_command(command)
                cron.get_next()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()