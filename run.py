import gspread
from google.oauth2.service_account import Credentials
import math
import statistics

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('forward_stock_plan')

# Other constants
PLANTERS = [
    'Roasted Almonds',
    'Salted Peanuts',
    'Mixed Nuts',
    'Honey Roasted Peanuts',
    'Cheez Balls',
    'Cashew'
]

RITTER = [
    'Rum Raisings Hazelnut',
    'Marzipan',
    'Whole Hazelnut',
    'Honey Salted Almonds'
]

WORKSHEET_TITLES = [
    'Weekly Sales',
    'Weekly Stocks',
    'Actual Deliveries',
    'Orders'
]


print(f'Welcome to the Forward Stock Plan Automation')

class ProductItem:
    def __init__(self, item_name, week_num, get_worksheet):
        self.item_name = item_name
        self.week_num = week_num
        self.get_worksheet = SHEET.worksheet(get_worksheet)

    def find_cell_value(self):
        item_row = self.get_worksheet.find(self.item_name)
        item_column = self.get_worksheet.find(str(self.week_num), in_row=8)
        item_cell_value = self.get_worksheet.cell(item_row.row, item_column.col).value

        return item_cell_value

class RowColumnValues:
    def __init__(self, value_sets):
        self.value_sets = value_sets
    
    def get_value_ranges(self):
        return self.value_sets

start_number = 9
end_number = 12

get_row_range = RowColumnValues([
    ProductItem(PLANTERS[2], number, WORKSHEET_TITLES[1]).find_cell_value()
    for number in range(start_number, end_number + 1)
])
item_row = get_row_range.get_value_ranges()
item_sale_row = [int(i) if isinstance(i, str) else 0 for i in item_row]
mean_weekly_sale = math.ceil(statistics.mean(item_sale_row))
print(item_sale_row)
print(mean_weekly_sale)


