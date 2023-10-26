import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_figures():
    '''
    Get sales figures input
    '''
    print('Please type in last sales figures')
    print('Figures should be six numbers, separated by commas')
    print('Example: 10,20,30,40,50,60\n')

    data_str = input('Enter figures here: ')
    print(f'The figures provided are {data_str}')

get_sales_figures()