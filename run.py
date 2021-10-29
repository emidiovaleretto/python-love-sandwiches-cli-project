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
    data_str = input('''
Please enter sales data from last market day.
Data should be six numbers, separated by commas.
Example: 10, 20, 30, 40, 50, 60
Enter your data here: ''')

    return f'The data provided is {data_str}'


data = get_sales_data()
print(data)