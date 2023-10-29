import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print('Please type in last sales figures')
        print('Figures should be six numbers, separated by commas')
        print('Example: 10,20,30,40,50,60\n')

        figures_str = input('Enter figures here: ')

        sales_figures = figures_str.split(',')

        if validate_figures(sales_figures):
            print('Valid values')
            break

    return sales_figures


def validate_figures(values):
    '''
    Try converting all string values into integers.
    Raises ValueError is strings cannot be converted into integers,
    or there aren't exactly 6 values
    '''      
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values are expected, but you provided {len(values)}'
            )
    except ValueError as error:
        print(f'Invalid data: {error}, please try again.\n')
        return False     
    return True


def update_worksheet(data, worksheet):
    '''
    Write surplus sandwiches into worksheet, adding new row 
    with listed updated figures.
    '''
    print(f'Update {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet.capitalize()} worksheet updated successfully.\n')


def calculate_surplus_sandwiches(sales_row):
    '''
    Compare sales with stock and calculate the surplus for each item type.

    the Surplus is defined as teh slaes figure subtract from stock:
    - Positive surplis idicates waste
    - Negative surplus idicates extra made when stock was sold out.
    '''
    print('Calculatting surplus sandwiches...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_sandwiches = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_sandwiches.append(surplus)
    return surplus_sandwiches


def main():
    '''
    Run program
    '''
    figures = get_sales_figures()
    converted_figures = [int(figure) for figure in figures]
    update_worksheet(converted_figures, 'sales')
    updated_stock = calculate_surplus_sandwiches(converted_figures)
    update_worksheet(updated_stock, 'surplus')


print('Welcome to Love Sandwiches Date Automation')
main()