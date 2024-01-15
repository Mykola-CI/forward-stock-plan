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
    'Deliveries',
    'Orders'
]

WEEKS_TO_FORECAST = 8

WEEKS_ROW_NUMBER = 1


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
    
    def cut_off_past_weeks(self, product, week_number):
        self.get_values()
        current_week_index = self.get_week_index(week_number)
        slice_product = [
        sublist for sublist in self.retrieved_values if product in sublist
    ]
        future_values = [row[current_week_index + 1:] for row in slice_product]
        future_numbers = [[int(x) if x != '' else 0 for x in sublist] for sublist in future_values]
        return future_numbers


def update_worksheet_data(worksheet, product, week_number, table_data):
    """
    Utility function. Updates given worksheet for a given Product Range with 
    data matrix 'table_data' passed in the form of list of lists. 
    Cells are updated from given 'Week Number + 1' in top left position
    """
    worksheet_instance = Worksheets(worksheet)
    gspread_object = worksheet_instance.get_gspread_worksheet()

    week_index = gspread_object.find(str(week_number), in_row=WEEKS_ROW_NUMBER)

    start_column = week_index.col + 1

    if product == PRODUCT_RANGE[0]:
        start_row = PLANTERS_START_ROW
    elif product == PRODUCT_RANGE[1]:
        start_row = len(PLANTERS) + PLANTERS_START_ROW + 1
    else:
        print('Product range input error or the Product range does not exist')

    start_cell_position = r1c1_to_a1(start_row, start_column)

    end_row = start_row + len(product)
    end_column = start_column + len(table_data[0])
    end_cell_position = r1c1_to_a1(end_row, end_column)
    cells_range = start_cell_position + ':' + end_cell_position

    gspread_object.update(cells_range, table_data)

    return None

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

    return average_sales


def update_sales_forecast(product, week_number):

    retrospective_average_sales = calculate_average_sales(
        product, week_number)

    sales_forecast = [
        [mean]*WEEKS_TO_FORECAST for mean in retrospective_average_sales
    ]

    update_worksheet_data(WORKSHEET_TITLES[0], product, week_number, sales_forecast)

    return None


def update_forward_stocks(product, week_number):

    print("Retrieving and processing data from the spreadsheet...")

    stocks = Worksheets(WORKSHEET_TITLES[1])
    stocks_values = stocks.cut_off_past_weeks(product, week_number - 1)
    sales = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales.cut_off_past_weeks(product, week_number - 1)
    deliveries = Worksheets(WORKSHEET_TITLES[2])
    deliveries_values = deliveries.cut_off_past_weeks(product, week_number - 1)

    print("Calculating forward stocks...")

    forward_stocks = []
    for i in range(len(stocks_values)):
        forward_stocks_row = [stocks_values[i][0] - sum(sales_values[i][:j+1]) + sum(deliveries_values[i][:j+1]) for j in range(len(sales_values[i])-1)]

        forward_stocks.append(forward_stocks_row)

    print("Updating the spreadsheet...")

    update_worksheet_data(WORKSHEET_TITLES[1], product, week_number, forward_stocks)

    return None

week_of_year = 1

print(f'Welcome to the Forward Stock Plan Automation')
x = 0
update_forward_stocks(PRODUCT_RANGE[x], week_of_year)
print(f"Forward Stock Plan has been updated for: {PRODUCT_RANGE[x]} \n from week: {week_of_year} and onward \n")




