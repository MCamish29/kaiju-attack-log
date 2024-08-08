import gspread
import colorama
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
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
    Get date of Kaiju attack input from the user.
    Run a while loop to collect valid date format from the user
    via terminal. The loop will repeat to request data, 
    until it is valid.
    """
    while True:
        print("Please enter date of Kaiju attack.")
        print("Date format should be dd/mm/yyyy.")
        print("Example: 01/01/2024\n")

        data_str = input("Enter date of Kaiju attack here: ")

        if validate_date(data_str):
            print(f"Confirmed, date of Kaiju attack is {data_str}")
            break

    return data_str           
            
    
def validate_date(date_str):
    """
    Raises ValueError if the date input is not in required format
    Colorama flags error message in red to signal to user of error
    """
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        print('\033[31m'+"Invalid date format. Please try again.\n")
        return False
    
def update_attack_log(data):
    """
    Updates Kaiju attack log to add date in relevant column
    """
    print("Importing date of Kaiju attack to log...\n")
    date_attack_log = SHEET.worksheet("attack_data")
    date_attack_log.append_row([data])
    print("Date of Kaiju attack logged successfully.\n")




data = get_date_data()
update_attack_log(data)