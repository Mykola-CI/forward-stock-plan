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


print(f'Welcome to the Forward Stock Plan Automation')

week_of_year = 4

def calculate_average_sales(product, week_number):

    print("Calc ave sales pulling data from the Weekly Sales worksheet")
    sales = SHEET.worksheet(WORKSHEET_TITLES[0]).get_all_values()
    print("Data obtained from the Weekly Sales worksheet")
    first_row = sales[0]
    current_week_index = first_row.index(str(week_number))

    product_range_sale = [sublist for sublist in sales if product in sublist]
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


test_sales = calculate_average_sales(PRODUCT_RANGE[1], week_of_year)

sales_forecast = [[mean]*WEEKS_TO_FORECAST for mean in test_sales]
print(f'The new list of forecasted sales:\n {sales_forecast}')







