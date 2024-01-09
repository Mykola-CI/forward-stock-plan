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

class RowValues:
    def __init__(self, row_values):
        self.row_values = row_values
    
    def get_row_values(self):
        return self.row_values

# item_sale_at_week = ProductItem('Mixed Nuts', 12, 'Weekly Sales').find_cell_value()    
# print(item_sale_at_week)

# item_stock_at_week = ProductItem('Mixed Nuts', 12, 'Weekly Stocks').find_cell_value()  
# print(item_stock_at_week)

get_row_range = RowValues([
    ProductItem('Mixed Nuts', 9, 'Weekly Sales').find_cell_value(),
    ProductItem('Mixed Nuts', 10, 'Weekly Sales').find_cell_value(),
    ProductItem('Mixed Nuts', 11, 'Weekly Sales').find_cell_value(),
    ProductItem('Mixed Nuts', 12, 'Weekly Sales').find_cell_value()
])
item_row = get_row_range.get_row_values()
item_sale_row = [int(i) for i in item_row]
mean_weekly_sale = math.ceil(statistics.mean(item_sale_row))
print(item_sale_row)
print(mean_weekly_sale)


