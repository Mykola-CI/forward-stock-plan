"""
Business and API related constants.
Refer to the README.md for more details.
"""

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
BRAND1 = [
    'Roasted Almonds',
    'Salted Peanuts',
    'Mixed Nuts',
    'Honey Roasted Peanuts',
    'Cheez Balls',
    'Cashew'
]


# RITTER SPORT PRODUCTS
BRAND2 = [
    'Rum Raisings Hazelnut',
    'Marzipan',
    'Whole Hazelnut',
    'Honey Salted Almonds'
]


# PRODUCT RANGES BY BRANDS FOR FURTHER ACCESS TO ITEMS:
PRODUCT_DICT = {PRODUCT_RANGE[0]: BRAND1, PRODUCT_RANGE[1]: BRAND2}


# MINIMUM ORDER QUANTITY IN RELATION TO SALES
SAFETY_MARGIN = 1.2


# MINIMUM STOCK LEVEL IN RELATION TO SALES
MIN_STOCK_LEVEL = 1.2


# LEAD TIMES
BRAND1_LT = 3
BRAND2_LT = 2


# The start row number for the Planters products
BRAND1_START_ROW = 3


# Number of weeks to update sales forecasts
WEEKS_TO_FORECAST = 8


# The row number for the weeks in the spreadsheet
WEEKS_ROW_NUMBER = 1
