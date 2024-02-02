"""
Constants for the menus, options and sub-options in the form of
lists of strings.
"""

from constants import *


MAIN_MENU_OPTIONS = [
    "[1] View Data",
    "[2] Update Weekly Sales",
    "[3] Update Orders",
    "[4] Glossary of Terms",
    "[5] Exit"
]


SUB_OPTIONS = [
    "[1] {}".format(PRODUCT_RANGE[0]),
    "[2] {}".format(PRODUCT_RANGE[1]),
    "[3] Back to Main Menu"
]


SUB_SUB_OPTIONS_VIEW = [
    "[1] Weekly Sales",
    "[2] Weekly Stocks",
    "[3] Deliveries",
    "[4] Orders",
    "[5] Back to Product Range"
]
