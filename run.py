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


def write_figures_into_worksheet(figures):
    '''
    Write figures into worksheet, adding new row with listed figures.
    '''
    print('Update sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(figures)
    print('Sales worksheet updated successfully.\n')


figures = get_sales_figures()
converted_figures = [int(figure) for figure in figures]
write_figures_into_worksheet(converted_figures)
