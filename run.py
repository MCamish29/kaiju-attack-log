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

        date_str = input("Enter date of Kaiju attack here: ")

        if validate_date(date_str):
            print(f"Confirmed, date of Kaiju attack is {date_str}\n")
            break

    return date_str           
            
    
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

def get_threat_data():
    """
    Get the threat level of Kaiju attack input from the user.
    Run a while loop to collect a valid threat level (1-5) from the user.
    The loop will repeat until a valid input is provided.
    """
    while True:
        print("Please enter the threat level of Kaiju attack.")
        print("Threat level is between 1 and 5.")
        print("1 is the lowest threat and 5 is the highest threat level\n")

        threat_str = input("Enter threat level of Kaiju attack here: ")

        if validate_threat_level(threat_str):
            print(f"Confirmed, threat level of Kaiju attack is {threat_str}\n")
            break

    return int(threat_str)  # return as an integer


def validate_threat_level(threat_str):
    """
    Validates that the threat level input is a number between 1 and 5.
    Raises ValueError if the input is not within this range.
    """
    try:
        threat_level = int(threat_str)
        if 1 <= threat_level <= 5:
            return True
        else:
            print('\033[31m' + "Invalid threat level. Please enter a number between 1 and 5.\n")
            return False
    except ValueError:
        print('\033[31m' + "Invalid input. Please enter a number between 1 and 5.\n")
        return False

data = get_date_data()
update_attack_log(data)
get_threat_data()