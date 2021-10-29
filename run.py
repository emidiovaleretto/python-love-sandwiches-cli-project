import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Returns sales figures imput from the user.
    """
    while True:
        data_str = input('''
Please enter sales data from last market day.
Data should be six numbers, separated by commas.
Example: 10, 20, 30, 40, 50, 60
Enter your data here: ''')

        data_list = data_str.split(',')

        is_valid = validate_data(data_list)

        if is_valid:
            print('Data is valid')
            break

    return data_list


def validate_data(values):
    """
    Validates the data input from the user.
    Inside the try/except block, the user is prompted 
    to enter the correct data. Raises a ValueError if 
    there aren't exactly six values.
    """
    try:
        [int(values) for values in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values must be entered and you provided '
                f'{len(values)} value(s)')

    except ValueError as err:
        print(f'Invalid data: {err}, please try again.')
        return False

    return True


data = get_sales_data()
print(data)