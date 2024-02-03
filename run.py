import math
import statistics
from simple_term_menu import TerminalMenu
from colorama import Fore, Back, Style
from constants import *
from menus import *
from service import *


def calculate_average_sales(product, sales_values, current_week_index):
    """
    Calculates average sales for a given product range and week number
    as a mean of sales for the last 5 weeks including the current week
    Return a list of integers.
    """
    # Slice the sales list of lists for a given product range.
    product_range_sale = [
        sublist for sublist in sales_values if product in sublist
    ]

    # Slice the last 5 weeks including the current week
    # Averages for the first 4 weeks sliced from index `0`.
    retrospective_sale_strings = [
        sublist[max(0, current_week_index - 4):current_week_index + 1]
        for sublist in product_range_sale
    ]

    # Convert the strings to integers by mapping `int` function
    # to items in the sub-lists. (Note: `sales_values` is
    # a list of lists of strings obtained from .get_values() method).
    retrospective_sales = [
        list(map(int, sublist)) for sublist in retrospective_sale_strings
    ]

    # Calculate the average sales for each product item wrapped in
    # the list comprehension.
    average_sales = [
        math.ceil(statistics.mean(lst)) for lst in retrospective_sales
    ]

    return average_sales


def update_sales_forecast(product, week_number):
    """
    Update Weekly Sales forecast based on the calculated averages
    and store the updated forecast to the Weekly Sales worksheet
    for a given product range and week number.
    """
    sales = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales.get_values()

    current_week_index = sales.get_week_index(week_number)

    retrospective_average = calculate_average_sales(
        product, sales_values, current_week_index
    )

    # Creates a list of lists by extrapolating the average sales
    # to the number of weeks set by the constant
    # `WEEKS_TO_FORECAST` or to the remaining weeks of a year.
    if week_number < 52 - WEEKS_TO_FORECAST:
        sales_forecast = [
            [mean]*WEEKS_TO_FORECAST for mean in retrospective_average
        ]
    else:
        sales_forecast = [
            [mean]*(52 - week_number) for mean in retrospective_average
        ]

    if week_number < 52:
        update_worksheet_data(
            WORKSHEET_TITLES[0], product, week_number+1, sales_forecast
        )

    return None


def calculate_stocks_for_item(
    from_index, sales_row, deliveries_row, stocks_row
):
    """
    Calculates future weekly stocks for an item (associated with
    a row in the worksheet) starting from a given index in the list
    to the end of that list. Returns a list of integers.
    """

    for k in range(from_index, len(sales_row)):
        if stocks_row[k-1] <= sales_row[k - 1]:
            stocks_row[k] = deliveries_row[k - 1]
        else:
            stocks_row[k] = (
                stocks_row[k - 1]
                + deliveries_row[k - 1]
                - sales_row[k - 1]
            )

    return stocks_row


def update_forward_stocks(product, week_number):
    """Calculate and store forward stock plan to
    the Weekly Stocks worksheet for a given product range
    starting from a given week to the end of year. Called each time
    when weekly sales forecast is updated without amending orders
    and deliveries.
    """

    stocks = Worksheets(WORKSHEET_TITLES[1])
    stocks_values = stocks.slice_past_weeks(product, week_number)
    sales = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales.slice_past_weeks(product, week_number)
    deliveries = Worksheets(WORKSHEET_TITLES[2])
    deliveries_values = deliveries.slice_past_weeks(product, week_number)

    forward_stock_plan = []
    for i in range(len(stocks_values)):
        forward_stock_plan.append(
            calculate_stocks_for_item(
                1, sales_values[i], deliveries_values[i], stocks_values[i]
            )
        )

    update_worksheet_data(
        WORKSHEET_TITLES[1], product, week_number, forward_stock_plan
    )

    return None


def calculate_orders(product, week_number):
    """
    Calculates orders recommendation for a given product range
    starting from a chosen week to the end of year.
    Updates deliveries plan and forward stock plan.
    Returns lists of lists for orders, deliveries and stocks.
    """

    forward_stocks_object = Worksheets(WORKSHEET_TITLES[1])
    forward_stocks_values = forward_stocks_object.slice_past_weeks(
        product, week_number
    )
    deliveries_object = Worksheets(WORKSHEET_TITLES[2])
    deliveries_values = deliveries_object.slice_past_weeks(
        product, week_number
    )
    sales_object = Worksheets(WORKSHEET_TITLES[0])
    sales_values = sales_object.slice_past_weeks(product, week_number)

    lead_time = define_lead_time(product)

    next_order = []
    deliveries = []
    stocks = []
    for i in range(len(sales_values)):
        sales_row = sales_values[i]

        # Create lists of zeros of the same length as the sales list
        # to clean the previous data which becomes irrelevant.
        orders_row = [0]*len(sales_row)
        deliveries_row = [0]*len(sales_row)
        stocks_row = [0]*len(sales_row)

        # Set deliveries for the goods already in transit
        # as these deliveries cannot be cancelled or amended.
        deliveries_row[:lead_time] = deliveries_values[i][:lead_time]

        # Set the initial stocks for the beginning of the current week
        # being actual values as opposed to those of the forward stocks.
        stocks_row[0] = forward_stocks_values[i][0]

        stocks_row = calculate_stocks_for_item(
            1, sales_row, deliveries_row, stocks_row
        )

        for j in range(len(sales_row)):

            # Calculate the average forecasted sales for the lead time+.
            ave_sale_lead_time = math.ceil(
                statistics.mean(sales_row[j:j+lead_time+2])
            )

            if stocks_row[j] < ave_sale_lead_time * (
                lead_time+1
            ) * MIN_STOCK_LEVEL:

                if j + lead_time + 1 < len(sales_row):
                    orders_row[j] = max(
                        math.ceil(
                            ave_sale_lead_time * SAFETY_MARGIN * (lead_time+1)
                        ) - stocks_row[j + lead_time + 1],
                        0
                    )
                    deliveries_row[j+lead_time] = orders_row[j]

                    # Update stocks for item when new delivery arises:
                    if deliveries_row[j+lead_time] != 0:

                        stocks_row = calculate_stocks_for_item(
                            j + lead_time,
                            sales_row,
                            deliveries_row,
                            stocks_row
                        )

                # These elif and else statements are for special
                # handling of the last weeks of year.
                elif j + lead_time + 1 == len(sales_row):
                    orders_row[j] = max(
                        math.ceil(
                            ave_sale_lead_time * (lead_time+1) * SAFETY_MARGIN
                        ) - (
                            stocks_row[j + lead_time]
                            - sales_row[j+lead_time]
                            + deliveries_row[j+lead_time]
                        ),
                        0
                    )
                    deliveries_row[j+lead_time] = orders_row[j]
                else:
                    orders_row[j] = max(
                        math.ceil(
                            ave_sale_lead_time * (lead_time+1) * SAFETY_MARGIN
                        ) - (
                                stocks_row[j]
                                - ave_sale_lead_time*(lead_time+1)
                                + sum(orders_row[j-lead_time:j+1])
                        ),
                        0
                    )
            # Stocks are sufficient and order is not needed.
            else:
                orders_row[j] = 0

        next_order.append(orders_row)
        deliveries.append(deliveries_row)
        stocks.append(stocks_row)

    return next_order, deliveries, stocks


def input_sales_for_week(product_range, week_number):
    """
    Prompts the user to input sales data for a given week number
    and returns the data as a list of lists: mimicking rows
    as product items and one column of sales.
    """

    week_sales = []
    product_items = PRODUCT_DICT[product_range]

    for item in product_items:
        while True:
            try:
                amount = int(
                    input(
                        f"\n Enter the amount for {item} sold in week "
                        f"{week_number} :\n"
                    )
                )
                if amount >= 0:
                    week_sales.append([amount])
                    break

                else:
                    print(
                        f"\n {Fore.RED}"
                        f"Sorry. The amount must be positive.\n"
                        f"{Style.RESET_ALL}"
                        f"\n Try again for {item}.")

            except ValueError as er:
                print(
                    f"\n {Fore.RED}"
                    f"You entered {er}. Please enter a positive "
                    "integer or 0."
                    f"{Style.RESET_ALL}"
                )

    return week_sales


def choose_week():
    """
    Prompt User to choose a week number and return
    the week number as integer.
    """
    while True:
        try:
            week_number = int(input("\n Enter the week number: \n"))
            if 1 <= week_number <= 52:
                break
            else:
                print(
                    f"\n {Fore.RED}"
                    f"Sorry. Week number must be between 1 and 52.\n"
                    f"{Style.RESET_ALL}"
                )
        except ValueError as err:
            print(
                f"\n {Fore.RED}"
                f"You entered {err}.\n Please enter a number "
                "between 1 and 52."
                f"{Style.RESET_ALL}"
            )

    return week_number


def run_update_sales(product):
    """
    Runs sequences and launches functions for updating sales data
    and storing them into the spreadsheet.
    """
    week_number = choose_week()
    week_sales = input_sales_for_week(product, week_number)

    update_worksheet_data(
        WORKSHEET_TITLES[0], product, week_number, week_sales
        )

    print(
        f"\n Sales for the week {week_number} have been stored "
        "to the spreadsheet.\n"
        )

    print("\n Updating sales forecast...")
    update_sales_forecast(product, week_number)
    print("\n Sales forecast has been updated.")

    lead_time = define_lead_time(product)

    if week_number < 52 - lead_time:
        print("\n Updating forward stocks...")
        update_forward_stocks(product, week_number)
        print("\n Forward stocks have been updated.")

    return None


def main():
    """Main function that runs menus and launches functions."""

    print(
        f"\n{Fore.GREEN}"
        f"""
        WELCOME TO THE FORWARD STOCK PLAN AUTOMATION
        --------------------------------------------
        Refer to the Glossary of Terms for guidance and definitions.
        """
        f"{Style.RESET_ALL}"
    )

    main_menu = TerminalMenu(
        MAIN_MENU_OPTIONS, title="\n Please choose an option:\n "
    )
    sub_view_menu = TerminalMenu(
        SUB_OPTIONS, title="\n Please choose a product range:\n"
    )
    sub_sub_view_menu = TerminalMenu(
        SUB_SUB_OPTIONS_VIEW, title="\n Please choose a worksheet to view:\n"
    )

    quit_program = False

    while quit_program is False:
        option_index = main_menu.show()
        option_choice = MAIN_MENU_OPTIONS[option_index]

        if (option_choice == MAIN_MENU_OPTIONS[-1]):
            clear_screen()

            quit_program = True
            print(
                f"\n{Fore.GREEN}"
                f"""
                Thank you for using the Forward Stock Plan Automation.
                ------------------------------------------------------
                """
                f"{Style.RESET_ALL}"
            )

        elif (option_choice == MAIN_MENU_OPTIONS[0]):
            clear_screen()
            print(Fore.GREEN + "View Data menu" + Style.RESET_ALL)
            sub_view_menu_index = sub_view_menu.show()
            sub_view_choice = SUB_OPTIONS[sub_view_menu_index]

            if (sub_view_choice == SUB_OPTIONS[0]):
                clear_screen()
                print(f"\n View Data for {PRODUCT_RANGE[0]} menu")
                sub_sub_view_menu_index = sub_sub_view_menu.show()
                sub_sub_view_choice = SUB_SUB_OPTIONS_VIEW[
                    sub_sub_view_menu_index
                ]

                if (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[0]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[0],
                        PRODUCT_RANGE[0],
                        week_number
                    )

                elif (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[1]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[1],
                        PRODUCT_RANGE[0],
                        week_number
                    )

                elif (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[2]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[2],
                        PRODUCT_RANGE[0],
                        week_number
                    )

                elif (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[3]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[3],
                        PRODUCT_RANGE[0],
                        week_number
                    )

                elif (
                    sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[4]
                ):
                    clear_screen()
                    pass

            elif (sub_view_choice == SUB_OPTIONS[1]):
                clear_screen()
                print(f"\n View Data for {PRODUCT_RANGE[1]} menu")

                sub_sub_view_menu_index = sub_sub_view_menu.show()
                sub_sub_view_choice = SUB_SUB_OPTIONS_VIEW[
                    sub_sub_view_menu_index
                ]

                if (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[0]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[0],
                        PRODUCT_RANGE[1],
                        week_number
                    )

                elif (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[1]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[1],
                        PRODUCT_RANGE[1],
                        week_number
                    )

                elif (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[2]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[2],
                        PRODUCT_RANGE[1],
                        week_number
                    )

                elif (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[3]):
                    week_number = choose_week()
                    print_table(
                        WORKSHEET_TITLES[3],
                        PRODUCT_RANGE[1],
                        week_number
                    )

                elif (sub_sub_view_choice == SUB_SUB_OPTIONS_VIEW[4]):
                    clear_screen()
                    pass

        elif (option_choice == MAIN_MENU_OPTIONS[1]):
            clear_screen()
            print(Fore.GREEN + "Update Weekly Sales menu" + Style.RESET_ALL)
            sub_update_index = sub_view_menu.show()
            sub_update_choice = SUB_OPTIONS[sub_update_index]

            if (sub_update_choice == SUB_OPTIONS[0]):
                clear_screen()
                print(
                    f"Update Weekly Sales for {PRODUCT_RANGE[0]} menu"
                )
                run_update_sales(PRODUCT_RANGE[0])

            elif (sub_update_choice == SUB_OPTIONS[1]):
                clear_screen()
                print(
                    f"Update Weekly Sales for {PRODUCT_RANGE[1]} menu"
                )
                run_update_sales(PRODUCT_RANGE[1])

            elif (sub_update_choice == SUB_OPTIONS[2]):
                clear_screen()
                pass

        elif (option_choice == MAIN_MENU_OPTIONS[2]):
            clear_screen()
            print(Fore.GREEN + "Update Orders menu" + Style.RESET_ALL)
            sub_update_index = sub_view_menu.show()
            sub_update_choice = SUB_OPTIONS[sub_update_index]

            if (sub_update_choice == SUB_OPTIONS[0]):
                clear_screen()
                print(
                    f"Update Orders for {PRODUCT_RANGE[0]} menu"
                )
                week_number = choose_week()

                print(
                    f"\n Calculating orders recommendation "
                    f"for {PRODUCT_RANGE[0]}...")
                next_order, deliveries, stocks = calculate_orders(
                    PRODUCT_RANGE[0], week_number
                    )

                print("\n Storing data to the spreadsheet...")

                update_worksheet_data(
                    WORKSHEET_TITLES[3],
                    PRODUCT_RANGE[0],
                    week_number,
                    next_order
                )
                update_worksheet_data(
                    WORKSHEET_TITLES[2],
                    PRODUCT_RANGE[0],
                    week_number,
                    deliveries
                )
                update_worksheet_data(
                    WORKSHEET_TITLES[1],
                    PRODUCT_RANGE[0],
                    week_number,
                    stocks
                )
                print(
                    f"\n Orders, deliveries and stocks for "
                    f"{PRODUCT_RANGE[0]} have been updated."
                )

            elif (sub_update_choice == SUB_OPTIONS[1]):
                clear_screen()
                print(
                    f"Update Orders for {PRODUCT_RANGE[1]} menu"
                )
                week_number = choose_week()

                print(
                    f"\n Calculating orders recommendation "
                    f"for {PRODUCT_RANGE[1]}...")
                next_order, deliveries, stocks = calculate_orders(
                    PRODUCT_RANGE[1], week_number
                )

                print("\n Storing data to the spreadsheet...")

                update_worksheet_data(
                    WORKSHEET_TITLES[3],
                    PRODUCT_RANGE[1],
                    week_number,
                    next_order
                )
                update_worksheet_data(
                    WORKSHEET_TITLES[2],
                    PRODUCT_RANGE[1],
                    week_number,
                    deliveries
                )
                update_worksheet_data(
                    WORKSHEET_TITLES[1],
                    PRODUCT_RANGE[1],
                    week_number,
                    stocks
                )
                print(
                    f"\n Orders, deliveries and stocks "
                    f"for {PRODUCT_RANGE[1]} have been updated.")

            elif (sub_update_choice == SUB_OPTIONS[2]):
                clear_screen()
                pass

        elif (option_choice == MAIN_MENU_OPTIONS[3]):

            clear_screen()
            print_glossary()

            input(
                "\n Scroll Up to see the beginning of the Glossary.\n"
                "\n Press Enter to return to the Main menu...\n")
            clear_screen()
            pass


if (__name__ == "__main__"):
    main()
