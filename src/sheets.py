import os
import gspread
import paramiko
import pandas as pd
from io import StringIO
from google.oauth2.service_account import Credentials
from utils import run_cmd, enter

def transfer_csv(session, remote_path, local_path):
    """
    Transfer a CSV file from the remote server to the local machine using SCP.

    :param session: Paramiko SSH session object
    :param remote_path: Path to the CSV file on the remote server (including filename)
    :param local_path: Path to save the CSV file locally (including filename)
    """
    try:
        scp = paramiko.SFTPClient.from_transport(session.get_transport())
        scp.get(remote_path, local_path)
        scp.close()
        print(f"Successfully transferred {remote_path} to {local_path}")
    except Exception as e:
        print(f"An error occurred during file transfer: {str(e)}")

def overwrite_csv_into_sheet(session, remote_path, sheet_url, local_path):
    """
    Transfers a CSV file from a remote Linux server via SCP, clears the existing data in the Google Sheet,
    and inserts the new data.

    :param session: Paramiko SSH session object
    :param remote_path: Path to the CSV file on the remote server (including filename)
    :param sheet_url: URL of the Google Sheet
    :param local_path: Path to save the CSV file locally (including filename)
    """
    try:
        # Transfer the CSV file from the remote server to the local machine
        transfer_csv(session, remote_path, local_path)

        # Read the CSV file from the local filesystem
        try:
            df = pd.read_csv(local_path, on_bad_lines='skip', sep=';')
        except pd.errors.EmptyDataError:
            print("The CSV file is empty. Skipping update.")
            return

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