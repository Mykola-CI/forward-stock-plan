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
PRODUCT_RANGE = ['PLANTERS', 'RITTER SPORT']
PLANTERS = [
    'Roasted Almonds',
    'Salted Peanuts',
    'Mixed Nuts',
    'Honey Roasted Peanuts',
    'Cheez Balls',
    'Cashew'
]

PLANTERS_START_ROW = 3

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

WEEKS_TO_FORECAST = 8


class Worksheets:
    def __init__(self, worksheet_to_get):
        self.worksheet_to_get = worksheet_to_get

    def get_values(self):
        self.retrieved_values = SHEET.worksheet(self.worksheet_to_get).get_all_values()
        return self.retrieved_values
    
    def get_week_index(self, week_number):
        first_row = self.retrieved_values[0]
        current_week_index = first_row.index(str(week_number))
        return current_week_index
    
    def get_gspread_worksheet(self):
        return SHEET.worksheet(self.worksheet_to_get)   


def r1c1_to_a1(row, col):

    cell = gspread.utils.rowcol_to_a1(row, col)

    return cell

def calculate_average_sales(product, week_number):

    sales = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales.get_values()

    current_week_index = sales.get_week_index(week_number)

    product_range_sale = [
        sublist for sublist in sales_values if product in sublist
    ]

    retrospective_sale_strings = [
        sublist[max(0, current_week_index - 4):current_week_index + 1]
        for sublist in product_range_sale
    ]

    retrospective_sales = [
        list(map(int, sublist)) for sublist in retrospective_sale_strings
    ]

    average_sales = [
        math.ceil(statistics.mean(lst)) for lst in retrospective_sales
    ]

    return current_week_index, average_sales


def update_sales_forecast(product, week_number):

    week_index, retrospective_average_sales = calculate_average_sales(
        product, week_number)

    sales_forecast = [
        [mean]*WEEKS_TO_FORECAST for mean in retrospective_average_sales
    ]

    sales = Worksheets(WORKSHEET_TITLES[0])
    sales_gspread = sales.get_gspread_worksheet()

    start_column = week_index + 2
    if product == PRODUCT_RANGE[0]:
        start_row = PLANTERS_START_ROW
    elif product == PRODUCT_RANGE[1]:
        start_row = len(PLANTERS) + PLANTERS_START_ROW + 1
    else:
        print('Product range input error or the Product range does not exist')

    start_cell_position = r1c1_to_a1(start_row, start_column)
    end_row = start_row + len(sales_forecast)
    end_column = start_column + len(sales_forecast[0])
    end_cell_position = r1c1_to_a1(end_row, end_column)
    cells_range = start_cell_position + ':' + end_cell_position

    print(f'Start and end cell positions converted: {cells_range}')

    sales_gspread.update(cells_range, sales_forecast)

    print(f'Sales forecast updated for {WEEKS_TO_FORECAST} weeks')



def update_forward_stocks(product, week_number):

    sales_values = SHEET.worksheet(WORKSHEET_TITLES[0]).get_all_values()
    deliveries_values = SHEET.worksheet(WORKSHEET_TITLES[2]).get_all_values()
    stocks = SHEET.worksheet(WORKSHEET_TITLES[1])
    stocks_values = stocks.get_all_values()

    first_row = sales_values[0]
    current_week_index = first_row.index(str(week_number))






week_of_year = 4

print(f'Welcome to the Forward Stock Plan Automation')

update_sales_forecast(PRODUCT_RANGE[1], week_of_year)

# week, sales_data = find_current_week_column(week_of_year)
# print(f'Index of the week in the unpacked sales worksheet: {week}')
# print(f'Sales list of lists:\n {sales_data}')

