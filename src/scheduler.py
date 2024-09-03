import yaml
import schedule
import time
import subprocess
import os

def load_executions(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def run_command(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)

def setup_schedules(executions):
    for execution in executions['executions']:
        schedule.every().day.at(execution['schedule']).do(run_command, execution['command'])

def main():
    executions_file = '/app/config/programmed_executions.yaml'
    executions = load_executions(executions_file)
    setup_schedules(executions)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()