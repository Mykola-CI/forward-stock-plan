import gspread
from google.oauth2.service_account import Credentials
import math
import statistics
from simple_term_menu import TerminalMenu

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


# CREDENTIALS, SCOPE, WORKING WITH GOOGLE SHEETS API
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('forward_stock_plan')

# WORKSHEET TITLES IN THE SPREADSHEET
WORKSHEET_TITLES = [
    'Weekly Sales',
    'Weekly Stocks',
    'Deliveries',
    'Orders'
]

# PRODUCT RANGES BY BRANDS:
PRODUCT_RANGE = ['PLANTERS', 'RITTER SPORT']

# PLANTERS PRODUCTS
PLANTERS = [
    'Roasted Almonds',
    'Salted Peanuts',
    'Mixed Nuts',
    'Honey Roasted Peanuts',
    'Cheez Balls',
    'Cashew'
]

# RITTER SPORT PRODUCTS
RITTER = [
    'Rum Raisings Hazelnut',
    'Marzipan',
    'Whole Hazelnut',
    'Honey Salted Almonds'
]

# PRODUCT RANGES BY BRANDS FOR FURTHER ACCESS TO ITEMS:
PRODUCT_DICT = {'PLANTERS': PLANTERS, 'RITTER SPORT': RITTER}

# MINIMUM ORDER QUANTITY IN RELATION TO SALES
SAFETY_MARGIN = 1.2

# MINIMUM STOCK LEVEL IN RELATION TO SALES
MIN_STOCK_LEVEL = 1.2

# UNITS PER CARTON
PLANTERS_UPC = 6
RITTER_UPC = 10

# LEAD TIMES
PLANTERS_LT = 3
RITTER_LT = 2

# The start row number for the Planters products
PLANTERS_START_ROW = 3

# Number of weeks to update sales forecasts
WEEKS_TO_FORECAST = 8

# The row number for the weeks in the spreadsheet
WEEKS_ROW_NUMBER = 1


class Worksheets:
    """
    Class for retrieving data from the worksheets in the spreadsheet
    """
    def __init__(self, worksheet_to_get):
        self.worksheet_to_get = worksheet_to_get

    def get_values(self):
        self.retrieved_values = SHEET.worksheet(self.worksheet_to_get).get_all_values()
        return self.retrieved_values
    
    def get_week_index(self, week_number):
        self.get_values()
        first_row = self.retrieved_values[WEEKS_ROW_NUMBER - 1]
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
        future_values = [row[current_week_index:] for row in slice_product]
        future_numbers = [[int(x) if x != '' else 0 for x in sublist] for sublist in future_values]

        return future_numbers


def update_worksheet_data(worksheet, product, week_number, table_data):
    """
    Utility function. Updates given worksheet for a given Product Range with 
    data matrix 'table_data' passed in the form of list of lists. 
    """
    worksheet_instance = Worksheets(worksheet)
    gspread_object = worksheet_instance.get_gspread_worksheet()

    week_index = gspread_object.find(str(week_number), in_row=WEEKS_ROW_NUMBER)

    start_column = week_index.col

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
    """
    Utility function. Converts given row and column numbers to A1 notation
    """
    cell = gspread.utils.rowcol_to_a1(row, col)

    return cell


def calculate_average_sales(product, sales_values, current_week_index):
    """
    Calculates average sales for a given product range and week number
    """
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
    """
    Updates the sales spreadsheet for a given product range and week number
    """
    sales = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales.get_values()

    current_week_index = sales.get_week_index(week_number)

    retrospective_average_sales = calculate_average_sales(
        product, sales_values, current_week_index)

    sales_forecast = [
        [mean]*WEEKS_TO_FORECAST for mean in retrospective_average_sales
    ]

    update_worksheet_data(WORKSHEET_TITLES[0], product, week_number+1, sales_forecast)

    return None


def calculate_forward_stocks(stocks_values, sales_values, deliveries_values):
    """
    Calculate and compose forward stock plan based on sales, deliveries and 
    stocks data
    """

    print("Calculating forward stocks...")

    forward_stocks = []
    for i in range(len(stocks_values)):
        forward_stocks_row = [stocks_values[i][0] - sum(sales_values[i][:j+1]) 
            + sum(deliveries_values[i][:j+1]) 
            for j in range(len(sales_values[i])-1)]

        forward_stocks.append(forward_stocks_row)
    
    forward_stock_plan = [[0 if num < 0 else num for num in sublist] 
                    for sublist in forward_stocks]

    return forward_stock_plan


def update_forward_stocks(product, week_number):

    print("Forward Stocks retrieving and processing data from the spreadsheet...")

    stocks = Worksheets(WORKSHEET_TITLES[1])
    stocks_values = stocks.cut_off_past_weeks(product, week_number)
    sales = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales.cut_off_past_weeks(product, week_number)
    deliveries = Worksheets(WORKSHEET_TITLES[2])
    deliveries_values = deliveries.cut_off_past_weeks(product, week_number)

    forward_stock_plan = calculate_forward_stocks(stocks_values, sales_values, deliveries_values)

    print(f"Updating forward stocks for {product} from week {week_number} onwards...")
    update_worksheet_data(WORKSHEET_TITLES[1], product, week_number+1, forward_stock_plan)

    print("Forward stocks have been updated.")

    return None

def calculate_orders(product, week_number):

    print("Orders retrieving and processing data from the spreadsheet...")

    forward_stocks_object = Worksheets(WORKSHEET_TITLES[1])
    forward_stocks_values = forward_stocks_object.cut_off_past_weeks(product, week_number)
    deliveries_object = Worksheets(WORKSHEET_TITLES[2])
    deliveries_values = deliveries_object.cut_off_past_weeks(product, week_number)
    # orders = Worksheets(WORKSHEET_TITLES[3])
    # orders_values = orders.cut_off_past_weeks(product, week_number)
    sales_object = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales_object.cut_off_past_weeks(product, week_number)

    print("Calculating orders...")

    if product == PRODUCT_RANGE[0]:
        lead_time = PLANTERS_LT
    elif product == PRODUCT_RANGE[1]:
        lead_time = RITTER_LT
    else:
        print('Product range input error or the Product range does not exist')

    next_order = []
    deliveries = []
    stocks = []
    for i in range(len(sales_values)):
        orders_row = [0]*len(sales_values[i])
        deliveries_row = [0]*len(sales_values[i])
        deliveries_row[:lead_time] = deliveries_values[i][:lead_time]
        stocks_row = [0]*len(sales_values[i])
        stocks_row[0] = forward_stocks_values[i][0]

        for k in range(1, len(sales_values[i])):
            if stocks_row[k-1] <= sales_values[i][k - 1]:
                stocks_row[k] = deliveries_row[k - 1]
            else:
                stocks_row[k] = stocks_row[k - 1] + deliveries_row[k - 1] - sales_values[i][k - 1]

        for j in range(len(sales_values[i])):
            ave_sale_lead_time = math.ceil(statistics.mean(sales_values[i][j:j+lead_time+2]))
            
            if stocks_row[j] < ave_sale_lead_time * (lead_time+1) * MIN_STOCK_LEVEL:
                
                if j + lead_time + 1 < len(sales_values[i]): 
                    orders_row[j] = max(math.ceil(ave_sale_lead_time * SAFETY_MARGIN * (lead_time+1)) - stocks_row[j + lead_time + 1], 0)
                    deliveries_row[j+lead_time] = orders_row[j]

                    if deliveries_row[j+lead_time] != 0:
                        for k in range(j + lead_time, len(sales_values[i])):
                            if stocks_row[k-1] <= sales_values[i][k - 1]:
                                stocks_row[k] = deliveries_row[k - 1]
                            else:
                                stocks_row[k] = stocks_row[k - 1] + deliveries_row[k - 1] - sales_values[i][k - 1]

                elif j + lead_time + 1 == len(sales_values[i]):
                    orders_row[j] = max(math.ceil(ave_sale_lead_time * (lead_time+1) * SAFETY_MARGIN) - (stocks_row[j + lead_time] - sales_values[i][j+lead_time] + deliveries_row[j+lead_time]), 0)
                    deliveries_row[j+lead_time] = orders_row[j]
                else:
                    orders_row[j] = max(math.ceil(ave_sale_lead_time * (lead_time+1) * SAFETY_MARGIN) - (stocks_row[j] - ave_sale_lead_time*(lead_time+1) + sum(orders_row[j-lead_time:j+1])), 0)
                    
            else:
                orders_row[j] = 0

        next_order.append(orders_row)
        deliveries.append(deliveries_row)
        stocks.append(stocks_row)

    return next_order, deliveries, stocks


def input_sales_for_week(product_range, week_number):
    """
    Prompts the user for sales data for a given week number and returns
    the data as a list of lists: rows as product items and one column of sales
    """

    week_sales = []
    product_items = PRODUCT_DICT[product_range]

    for item in product_items:
        while True:
            try:
                amount = int(input(f"Enter the amount for '{item}' sold in week {week_number}: "))
                week_sales.append([amount])
                if amount >= 0:
                    break
                else:
                    print(f"Sorry. The amount must be positive. Try again for '{item}'.")
            except ValueError as er:
                print(f"You entered {er}. Please enter a positive integer or 0.")

    return week_sales


def choose_week():
    """
    Prompts the user to choose a week number and returns the number
    """
    while True:
        try:
            week_number = int(input("Enter the week number: "))
            if 1 <= week_number <= 52:
                break
            else:
                print("Sorry. Week number must be between 1 and 52.")
        except ValueError as err:
            print(f"You entered {err}. Please enter a number between 1 and 52.")
    
    return week_number

def run_update_data(product_range):
    """
    Runs the update data function
    """
    week_number = choose_week()
    week_sales = input_sales_for_week(product_range, week_number)

    # update_worksheet_data(
    #     WORKSHEET_TITLES[0], product_range, week_number, week_sales
    #     )
    
    print(f"Sales for the week {week_number} have been updated to the spreadsheet.")


    return None

def main():
    """Main function"""

    print(f'Welcome to the Forward Stock Plan Automation')
    

    main_menu_options = ["[1] View Data", "[2] Update Data", "[3] Exit"]
    sub_menu_options = ["[1] for Planters", "[2] for Ritter Sport", "[3] Back to Main Menu"]

    main_menu = TerminalMenu(main_menu_options, title="What to begin with? Please choose an option:")
    sub_menu = TerminalMenu(sub_menu_options, title="Please choose a product range:")

    quit_program = False

    while quit_program == False:
        option_index = main_menu.show()
        option_choice = main_menu_options[option_index]

        if(option_choice == "[3] Exit"):
            quit_program = True
            print("Thank you for using the Forward Stock Plan Automation. See ya!")
        elif(option_choice == "[1] View Data"):
            print("View Data")
        elif(option_choice == "[2] Update Data"):
            sub_option_index = sub_menu.show()
            sub_option_choice = sub_menu_options[sub_option_index]
            if(sub_option_choice == "[1] for Planters"):
                run_update_data(PRODUCT_RANGE[0])
            elif(sub_option_choice == "[2] for Ritter Sport"):
                run_update_data(PRODUCT_RANGE[1])
            elif(sub_option_choice == "[3] Back to Main Menu"):
                print("Back to Main Menu")

            # update_worksheet_data(WORKSHEET_TITLES[0], chosen_range, week_number, week_sales)

main()
