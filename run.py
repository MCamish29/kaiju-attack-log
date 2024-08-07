import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('kaiju_attack_log')

def get_date_data():
    """
    Get date of Kaiju attack input from the user
    """
    print("Please enter date of Kaiju attack.")
    print("Date format should be dd/mm/yyyy.")
    print("Example: 01/01/2024\n")

    data_str = input("Enter date of Kaiju attack here:")
    print(f"Confirmed, date of attack is {data_str}")

get_date_data()