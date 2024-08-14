import gspread
import colorama
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style
from datetime import datetime

colorama.init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('kaiju_attack_log')

REGION = {
    "1": "Asakusa",
    "2": "Ginza",
    "3": "Harajuku",
    "4": "Shibuya",
    "5": "Shinjuku",
    "6": "Other"
}


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

        date_str = input("Enter date of Kaiju attack here:\n").strip()

        if validate_date(date_str):
            print(Fore.GREEN
                  + f"Confirmed, date of Kaiju attack is {date_str}\n")
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

        threat_str = input("Enter threat level of Kaiju attack here:\n").strip()

        if validate_threat_level(threat_str):
            print(Fore.GREEN
                  + f"Confirmed, threat level of Kaiju attack is {threat_str}")
            print()
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
            print('\033[31m'
                  + "Invalid threat level."
                  + "Please enter a number between 1 and 5")
            print()
            return False
    except ValueError:
        print('\033[31m'
              + "Invalid input."
              + "Please enter a number between 1 and 5.\n")
        return False


def get_region_data():
    """
    Get the region of Kaiju attack input from the user.
    Run a while loop to collect a valid region (1-6) from the user.
    The loop will repeat until a valid input is provided.
    """
    while True:
        print("Please enter the region of Kaiju attack.")
        print("Select the number associated with the relevant region:")
        print("1 = Asakusa, "
              + "2 = Ginza, "
              + "3 = Harajuku, "
              + "4 = Shibuya, "
              + "5 = Shinjuku, "
              + "6 = Other\n")

        region_str = input("Enter the region of Kaiju attack here:\n").strip()

        if validate_region(region_str):
            region_name = REGION[region_str]
            print(Fore.GREEN
                  + f"Confirmed, region of Kaiju attack is {region_name}\n")
            return region_name


def validate_region(region_str):
    """
    Validates that the region input is a number between 1 and 6.
    Raises ValueError if the input is not within this range.
    """
    try:
        region_num = int(region_str)
        if 1 <= region_num <= 6:
            return True
        else:
            print('\033[31m'
                  + "Invalid region number. "
                  + "Please enter a number between 1 and 6.\n")
            return False
    except ValueError:
        print('\033[31m'
              + "Invalid input. "
              + "Please enter a valid number between 1 and 6.\n")
        return False


def update_attack_log(date, threat_level, region_name):
    """
    Updates Kaiju attack log
    Function will add date, threat level, and region name in relevant columns.
    """
    print("Importing date, "
          + "threat level, "
          + "and region of Kaiju attack to log...\n")
    attack_log_worksheet = SHEET.worksheet("attack_data")
    attack_log_worksheet.append_row([date, threat_level, region_name])
    print(Fore.GREEN + "Kaiju attack logged successfully.\n")


def return_last_entry():
    """
    Returns the last entry from the 'attack_data' worksheet.
    """
    attack_log_worksheet = SHEET.worksheet("attack_data")
    last_entry = attack_log_worksheet.get_all_values()[-1]
    return last_entry
    

# Main flow
def start_program():
    """
    Greets users with an introduction to the terminal.
    Instructions are displayed for what the user can expect.
    """

    print("Welcome to the Kaiju attack log terminal\n")
    print("This terminal is designed to "
          + "log reports of Kaiju attacks in Tokyo.\n")
    print("If you select to enter a new entry "
          + "you will need to enter the following criteria:")
    print("'date' in dd/mm/yyyy format,")
    print("'threat level' ranging from 1 to 5,")
    print("'region of attack'\n")
    start_program_str = input("To log a new entry enter 'new', "
                              + "to display the previous entry "
                              + "enter 'return':\n").strip().lower()
    print()

    if start_program_str == "new":
        attack_log()
    elif start_program_str == "return":
        last_entry = return_last_entry()
        print("Returning previous entry:\n")
        print(f"Date: {last_entry[0]}")
        print(f"Threat Level: {last_entry[1]}")
        print(f"Region: {last_entry[2]}\n")
        additional_entry()
    else:
        print('\033[31m' + "Invalid input. Please enter 'new' or 'return'.\n")
        start_program()  # Restart the program if input is invalid


def attack_log():
    date = get_date_data()
    threat_level = get_threat_data()
    region_name = get_region_data()
    update_attack_log(date, threat_level, region_name)
    additional_entry()


def additional_entry():
    """
    Allows to user to enter additional entry or return to main menu
    if, elif and else being used for validation.
    """
    print("Would you like to log another attack?")
    additional_entry_str = input("Please enter 'Y' to log another attack "
                                 + "or 'N' to return "
                                 + "to menu:\n").strip().lower()
    print()
    if additional_entry_str == "y":
        attack_log()
    elif additional_entry_str == "n":
        start_program()
    else:
        print('\033[31m' + "Invalid input. Please enter 'Y' or 'N'.\n")
        additional_entry()


if __name__ == "__main__":
    start_program()
