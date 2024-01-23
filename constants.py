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
