import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from io import StringIO
from utils import run_cmd, enter
import os

def append_csv(session, remote_path, sheet_url):
    """
    Reads a CSV file from a remote Linux server via SSH and appends its data to a Google Sheet.

    :param session: Paramiko SSH session object
    :param remote_path: Path to the CSV file on the remote server (including filename)
    :param sheet_url: URL of the Google Sheet
    """
    try:
        # Navigate to the directory containing the CSV file
        directory = '/'.join(remote_path.split('/')[:-1])
        filename = remote_path.split('/')[-1]
        run_cmd(session, f"cd {directory}" + enter())

        # Use 'cat' command to output the content of the CSV file
        csv_content = run_cmd(session, f"cat {filename}" + enter())

        # Create a DataFrame from the CSV content
        df = pd.read_csv(StringIO(csv_content))

        # Set up credentials
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the service account JSON file (one level up)
        service_account_path = os.path.join(current_dir, '..', 'google-credentials.json')

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(service_account_path, scopes=scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet
        sheet = client.open_by_url(sheet_url).sheet1

        # Convert DataFrame to list of lists
        values = df.values.tolist()

        # Append the data to the sheet
        sheet.append_rows(values)

        print(f"Successfully appended {len(values)} rows to the Google Sheet.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def overwrite_csv(session, remote_path, sheet_url):
    """
    Reads a CSV file from a remote Linux server via SSH, clears the existing data in the Google Sheet,
    and inserts the new data.

    :param session: Paramiko SSH session object
    :param remote_path: Path to the CSV file on the remote server (including filename)
    :param sheet_url: URL of the Google Sheet
    """
    try:
        # Navigate to the directory containing the CSV file
        directory = '/'.join(remote_path.split('/')[:-1])
        filename = remote_path.split('/')[-1]
        run_cmd(session, f"cd {directory}" + enter())

        # Use 'cat' command to output the content of the CSV file
        csv_content = run_cmd(session, f"cat {filename}" + enter())

        # Create a DataFrame from the CSV content
        df = pd.read_csv(StringIO(csv_content))

        # Set up credentials
        current_dir = os.path.dirname(os.path.abspath(__file__))
        service_account_path = os.path.join(current_dir, '..', 'service_account.json')

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(service_account_path, scopes=scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet
        sheet = client.open_by_url(sheet_url).sheet1

        # Clear existing data
        sheet.clear()

        # Convert DataFrame to list of lists, including column headers
        values = [df.columns.tolist()] + df.values.tolist()

        # Insert the data to the sheet
        sheet.update(values)

        print(f"Successfully cleared existing data and inserted {len(values) - 1} rows to the Google Sheet.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")