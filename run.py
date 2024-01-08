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
SHEET = GSPREAD_CLIENT.open('forward_stock_plan')

sales = SHEET.worksheet('Weekly Sales')

# data = sales.col_values(3)
# print(data)

some_values = [
    [22, 33],
    [16, 17],
    [19, 20],
    [110, 120]
]
sales.update(range_name='O10:P13', values=some_values)

print(f'Just trying to print some values: {some_values}')




