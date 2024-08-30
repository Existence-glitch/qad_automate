import os
import csv
import gspread
import paramiko
from datetime import datetime
from google.oauth2.service_account import Credentials

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

def clean_value(value):
    """Clean and convert value to appropriate type."""
    value = value.strip()
    try:
        # Try converting to float
        return float(value)
    except ValueError:
        # If not a number, return as string
        return value

def format_date(date_string):
    """Convert date string to YYYY-MM-DD format."""
    try:
        date = datetime.strptime(date_string, '%m/%d/%y')
        return date.strftime('%Y-%m-%d')
    except ValueError:
        return date_string
    
def read_csv_with_encoding(file_path, encodings=['utf-8-sig', 'latin-1', 'iso-8859-1', 'windows-1252']):
    """Try to read CSV file with different encodings."""
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                csv_reader = csv.reader(file, delimiter=';')
                data = list(csv_reader)
            print(f"Successfully read the file with {encoding} encoding.")
            return data
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to read the CSV file with any of the specified encodings.")

def insert_csv_to_googlesheet(csv_path, sheet_url, sheet_name=None, debug=False):
    """
    Reads a CSV file and inserts its contents into a Google Sheet using csv library.

    :param csv_path: Path to the CSV file
    :param sheet_url: URL of the Google Sheet
    :param sheet_name: Name of the sheet to insert data into (optional)
    :param debug: If True, display CSV contents before insertion (default False)
    """
    try:
        # Set up credentials
        current_dir = os.path.dirname(os.path.abspath(__file__))
        service_account_path = os.path.join(current_dir, '..', 'google-credentials.json')
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(service_account_path, scopes=scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet
        sheet = client.open_by_url(sheet_url)

        # Select the worksheet
        if sheet_name:
            try:
                worksheet = sheet.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                print(f"Worksheet '{sheet_name}' not found. Creating it.")
                worksheet = sheet.add_worksheet(title=sheet_name, rows="100", cols="20")
        else:
            worksheet = sheet.get_worksheet(0)  # Get the first sheet

        # Read the CSV file
        raw_data = read_csv_with_encoding(csv_path)
        headers = raw_data[0]
        data = [headers]

        date_columns = ['Fecha ETD', 'Fecha ETA Cliente', 'Fch.Produc.', 'Fch.Venc.']
        date_indices = [headers.index(col) for col in date_columns if col in headers]

        for row in raw_data[1:]:
            cleaned_row = [clean_value(value) for value in row]
            for idx in date_indices:
                if idx < len(cleaned_row):
                    cleaned_row[idx] = format_date(cleaned_row[idx])
            data.append(cleaned_row)

        if debug:
            print("CSV contents:")
            for row in data[:5]:  # Print first 5 rows for debugging
                print(row)

        # Clear existing content and insert new data
        worksheet.clear()
        worksheet.update(data)

        print(f"Successfully inserted data from {csv_path} into the Google Sheet.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()