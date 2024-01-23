import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style
from tabulate import tabulate
from constants import *


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


class Worksheets:
    """
    The Class to serve as a Major intermediary between the project logic
    and the Google Sheet API. Retrieves objects and data from the API.
    Truncates the data and returns it to the project logic.
    """

    def __init__(self, worksheet_to_get):
        self.worksheet_to_get = worksheet_to_get

    # gets all values from the worksheet in the form of list of lists
    def get_values(self):
        self.retrieved_values = SHEET.worksheet(
            self.worksheet_to_get).get_all_values()
        return self.retrieved_values

    # gets the index of the week number in the retrieved list of lists
    def get_week_index(self, week_number):
        self.get_values()
        first_row = self.retrieved_values[WEEKS_ROW_NUMBER - 1]
        current_week_index = first_row.index(str(week_number))
        return current_week_index

    # gets the worksheet object from the Google Sheet API
    def get_gspread_worksheet(self):
        return SHEET.worksheet(self.worksheet_to_get)

    # Slice the columns of the worksheet from the given week number.
    # The goal is to optimize the computation time when iterating
    def slice_past_weeks(self, product, week_number):
        self.get_values()
        current_week_index = self.get_week_index(week_number)
        slice_product = [
            sublist for sublist in self.retrieved_values if product in sublist
        ]
        future_values = [row[current_week_index:] for row in slice_product]

        future_numbers = [
            [int(x) if x != '' else 0 for x in sublist]
            for sublist in future_values
        ]

        return future_numbers


def transform_cell_coordinates(row, col):
    """
    Utility function. Converts given row and column numbers
    (in so called R1C1 notation) to the alternative notation with
    columns represented by letters (so called A1B1 notation).
    A1B1 notation is required for some methods in the gspread module.
    """
    cell = gspread.utils.rowcol_to_a1(row, col)

    return cell


def update_worksheet_data(worksheet, product, week_number, table_data):
    """
    Utility function. Transfers the passed list of lists to
    the required worksheet for a given Product Range and
    from given Week Number onwards.
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
        print(
            "Product range input error or the Product range"
            "does not exist")

    start_cell_position = transform_cell_coordinates(
        start_row, start_column
    )

    end_row = start_row + len(product)
    end_column = start_column + len(table_data[0])
    end_cell_position = transform_cell_coordinates(end_row, end_column)

    cells_range = start_cell_position + ':' + end_cell_position

    gspread_object.update(cells_range, table_data)

    return None


def print_table(worksheet, product_range, week_number):
    """
    Prints the table of the chosen worksheet (sales, stocks, orders,
    or deliveries for a given product range and week number
    """
    worksheet_instance = Worksheets(worksheet)
    worksheet_values = worksheet_instance.slice_past_weeks(
        product_range, week_number
    )

    # transpose the table to print it vertically using '*' unpacking
    # and zip() function to pair the values
    turn_table_vertical = list(zip(*worksheet_values))

    product_items = PRODUCT_DICT[product_range]
    row_ids = [week_number + i for i in range(len(worksheet_values[0]))]
    print(
        f"""
        {worksheet} for {product_range} as from the week {week_number}:
        """
    )
    print(
        tabulate(
            turn_table_vertical, headers=product_items, showindex=row_ids,
            tablefmt='fancy_grid', maxheadercolwidths=8,
            colalign=("center",)*(len(product_items)+1)
        )
    )

    return None


def print_glossary():
    """
    Prints the glossary of terms from the glossary.txt file
    """
    with open('glossary.txt', 'r') as file:
        glossary_text = file.read()
        print(glossary_text)

    return None


def define_lead_time(product):
    """
    Defines the lead time for the given product range
    """
    if product == PRODUCT_RANGE[0]:
        lead_time = PLANTERS_LT
    elif product == PRODUCT_RANGE[1]:
        lead_time = RITTER_LT
    else:
        print(
            'Product range input error or'
            'the Product range does not exist')

    return lead_time
