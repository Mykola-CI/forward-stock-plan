# FORWARD STOCK PLAN AUTOMATION

Forward Stock Plan Automation is a Python terminal program, which is designed to aid to logistic and supply function of distribution and wholesaling companies in order to manage their stock levels and place timely orders. This business process is an everyday job if a distributor strives to avoid out-of-stock situations. An automation of the process becomes a must-have tool for importers, distributors and wholesalers.

The project can be observed and tested [here](https://forward-stock-plan-73f29ce621b0.herokuapp.com/)

![Mock screens of the application deployed via Heroku](documentation/mock-screens-heroku.png)

## Business Context
Once there is always a non-zero time between placing an order and a delivery of an item the inbound logistics of any business will face a problem of proper stocks control. Such time when the goods are actually in transit is usually called by distributors "__a lead time__". The problem becomes an essential challenge for a business when marketing cycle of that business is comparable to lead times and sometimes may take more then one week, or several weeks or even more than a month (for example, as regards the imports from China)

I developed this application aiming at automation of this process for mid-size and smaller businesses that cannot afford the expensive software and try to cope with the task by means of Excel or other spreadsheet applications.

A Python-based system can offer significant advantages over a purely Excel-based system in terms of data handling, integration with other systems, customization, scalability and data protection. Python can automate mundane tasks, making them much more efficient. This is particularly useful for tasks such as updating sales forecasts, calculating order recommendations, and controlling stock levels. Automation can reduce the risk of human error, increase efficiency, and free up time for more strategic tasks.

Basically, what the application does can be briefly described as follows:

- updates weekly sales forecasts based on actual sales input and retrospective sales
- calculates forward stock plan (future stocks) at the beginning of every coming week to the end of a year and based on weekly  delivery plan
- calculates orders recommendations: quantities per item and time for placement
- updates delivery plan after any change in orders 
- updates forward stock plan based on new order plan and/or sales forecast

At the current version of the application there are 2 product ranges used as templates: 
- Planters nuts with 6 product items
- Ritter Sport chocolate bars with 4 product items

The application assumes easy settings for adding both new product ranges and new product items within a range.

## Glossary Of Terms
    
    "Product Ranges" - product items under one umbrella brand.
    Currently there are two product ranges: Planters and
    Ritter Sport

    "Week Number" - the number of the week in the year
    
    "Weekly Sales" - the number of units sold in the chosen week
    or with regards to future weeks - sales forecast

    "Weekly Stocks" - the number of units in stock at 
    (important!) the beginning of the week

    "Orders" - the number of units to be ordered in 
    a particular week (recommendation) taking into
    consideration the lead time of particular Product Range

    "Deliveries" - the number of units delivered in 
    the past week or with regards to future weeks - 
    to be delivered at the estimated week of delivery

    "Lead Time" - the number of weeks between placing 
    the order and receiving the delivery. The delivered
    goods become available for sale only from the next week
    after estimated arrival (Lead Time + 1)

    "Forward Stock Plan" - the number of units in stock 
    estimated for all future weeks at the current rate of 
    sales and expected deliveries

    "Safety Margin" - the percentage of additional units to 
    order on top of the average sales to avoid stockouts

    "Minimum Stock Level" - the multiple of average sales
    to keep in stock to avoid stockouts

## Features
The application is run in terminal. Once being launched it displays a welcome message and a main menu.

### Navigating menus

![Main Menu](documentation/main-menu.png)

- Main menu
    - _[1] View Data_ - view sales, stocks, orders, deliveries
    for a given product range and week number. Data is 
    presented in a table format for all weeks from the
    chosen week number to the end of year

    - _[2] Update Weekly Sales_ - type in sales for the chosen
    product range and week. The data can be updated 
    for any chosen week to record either actual sales or 
    update forecasts. Once all items for the product range 
    have been typed in, the application calculates and updates 
    sales forecast and stocks.    
    Both Sales and Stocks are then stored in
    their respective worksheets

    - [3] _Update Orders_ - calculate orders recommendation 
    based on new sales, stocks and deliveries data for a 
    given week number and product range. Updates Orders, 
    Deliveries, and Stocks to the respective worksheets

    - [4] _Glossary of Terms_ - basic glossary which provides guidance 
    on using options of the menu and terminology definitions

    - [5] _Exit_ - The correct way to exit the application without hard reset

-  _[1] View Data_, _[2] Update Weekly Sales_, [3] _Update Orders_ sub-menu, which is common for these 3:
    - choose the product range to work with in order to View Data, Update Weekly Sales or Update Orders.

![Sub-menus](documentation/sub-menu-products.png)

- Main Menu Chart

```mermaid
flowchart TB
A[Main Menu]-->AB(View data)
A-->AC(Update Weekly Sales)
A-->AD(Update Orders)
A-->AE(Glossary of Terms)
A-->AF(Exit)
AB-->ABP(Choose Product Range<br>sub-menu)
AC-->ABP
AD-->ABP
```
-------------------
- View Data sub-menu

```mermaid
flowchart TB
A[Main Menu]-->AB(View Data<br>sub-menu)
AB-->ABP(Choose Product Range<br>sub-menu)
ABP-->WS(Weekly Sales)
ABP-->WSt(Weekly Stocks)
ABP-->D(Deliveries)
ABP-->O(Orders)
AB-->B(Back To The Main menu)
B-->A
WS-->W[[Choose Week Number <br>Type in the number between 1 and 52]]
WSt-->W
D-->W
O-->W
W--->TD[(Table Data displayed in terminal:<br> Rows- Product Items/ Columns- Week Numbers)]
TD-.-P([The data is presented for the period<br> from the chosen week to the end of year])
TD--Main Menu <br> appears under <br> the displayed table-->A

```

![View data Sub-menu](documentation/view-data-sub-menu.png)
![Display Table data](documentation/table-display.png)
--------------------------------
- Update Weekly Sales sub-menu

```mermaid
flowchart TB
A[Main Menu]-->AC
AC(Update Weekly Sales<br>sub-menu)-->ABP(Choose Product Range<br>sub-menu)
ABP-->W[[Choose Week Number <br>Type in the number between 1 and 52]]
W-->TYPE[[Type in Number of Units Sold for Chosen Week <br> one by one for each item]]
CALC--Main Menu<br> appears after <br>updating data-->A
TYPE-.-CALC([Calculation of Average Sales<br>Updating Sales Forecast<br>Updating Forward Stock Plan])
```
----------------
- Update Orders sub-menu

```mermaid
flowchart TB
A[Main Menu]-->AD
AD(Update Orders<br>sub-menu)-->ABP(Choose Product Range<br>sub-menu)
ABP-->W[[Choose Week Number<br>Type in the number between 1 and 52]]
W-.-CAO([Calculates Orders Recommendation <br>Updates Plan of Deliveries<br>Update forward Stock Plan Stocks])
CAO--Main Menu<br> appears after<br> all calculations<br>are stored-->A
```
### Future features
The application requires more time to develop and enhance features.
- Allow user to change Safety Margin and Minimum Stock level Constants via terminal window.

Currently it may be done relatively easy by a software programmer making changes to dedicated file 'constants.py'

- Allow user to update sales forecasts manually for all desired weeks for a particular item apart from automated sales forecast calculation

Currently it can be done manually by typing in sales for one column/week at a time. User must be given option for multiple input by row, i.e. by product item for multiple weeks in one go

- Allow user to input actual stocks on a weekly basis to account for discrepancies between planned and actual deliveries and shortages/surplus 

- Provide for smooth transition from year to year, set a procedure to submit past year and open next year

Currently the application deals with the beginning and the end of the year mostly with purpose to prevent from bugs or the program crushing. For example, in the beginning of the year retrospective sales are taken only from the week 1, whereas the automated forecasts, either sales or orders with deliveries are ended by week 52. The weeks closer than the lead time+1 before and after the year end are handled specially.  

## Data Model

The Data Model for the Forward Stock Plan Automation project is designed to efficiently manage and automate stock levels control by interacting with Google Sheets and processing data through a Python-based logic module. The rationale behind this model is to leverage the accessibility and simplicity of Google Sheets while utilizing Python for its powerful data manipulation capabilities.

__Major Blocks__

- Google Sheets:

  - Serves as a cost-effective, cloud-based storage system for data in tabular format.
  - Acts as a pseudo-database, accessible and editable by users.

![Weekly sales Worksheet](documentation/weekly-sales-workbook.png)
![Weekly Stocks Worksheet](documentation/weekly-stocks-workbook.png)
![Orders Worksheet](documentation/orders-workbook.png)
![Deliveries Worksheet](documentation/deliveries-workbook.png)


- Project Logic Module:
  - Contains functions that perform calculations and data processing according to business requirements.
  - Ensures that the business logic is encapsulated within the project, separate from data storage.

__Intermediary Python Class__

- A Python class named Worksheets acts as an intermediary between the project logic and the Google Sheets. API
- Responsibilities of the Worksheets class include:
    - Retrieving data from Google Sheets (Weekly Sales, Weekly Stocks, Deliveries, Orders).
    - Preparing data for processing by the logic module.
    - Returning processed data for storage back into the Google Sheets.

__Class Instances and Methods__

- Instances of the __Worksheets__ class represent individual worksheets, such as Sales, Stocks, Deliveries and Orders.
- The class can handle worksheets as objects or as lists of lists, which mimic tables with rows and columns in Python.
- Methods within the class include:
  - Defining columns for specific weeks.
  - Slicing data from past weeks.
  - Converting string data to integers for processing.

__Auxiliary and Utility Functions__

- Additional functions support the Worksheets class and facilitate interaction with the Google Sheets API.
- Examples include:
  - Converting cell notation (R1C1 to A1B1).
  - Updating and writing values to a range of cells in Google Sheets.
- Other functions, which might be considered as utilities include:
  - print data into terminal using _tabulate_ module
  - clear terminal screen
  - some other minor utilities 


__Minimization of API Calls__
- The data model is optimized to minimize the number of Google Sheets API calls
- The .get_all_values() method is used to retrieve all necessary data in a single call.
- All manipulations and calculations are performed within the Python environment, without additional API calls.
- Processed data is then stored back to the worksheet in one action, reducing the load on the API and improving performance.

```mermaid
flowchart LR
P[FSP Code]-.-GET>Get data]-.-G
P<-->CLASS[/class Worksheets:\]<-->G[(Google<br> Sheets)]
P-.-PUSH>Push Data]-.-G

```

__Rationale__

The main purpose of the Data Model is to retrieve, process, and store back data related to sales, stocks, deliveries, and orders. The chosen model is structured to:
- __Maximize Efficiency__: By minimizing API calls, the model reduces latency and potential rate limits associated with frequent data retrieval and updates
- __Enhance Organization__: The separation of data storage (Google Sheets) and processing logic (Python module) ensures a clean architecture and easier maintenance.
- __Improve Scalability__: The use of Python allows for complex data processing that can be scaled as business requirements grow.
- __Ensure Accessibility__: Google Sheets provides a user-friendly interface for non-technical users to view and input data, while the backend processing remains robust and automated.

## Testing
### Validator Testing. PEP8 Linter

- run.py

![run.py](documentation/pep8/run.png)

- service.py

![service.py](documentation/pep8/service.png)

- menus.py

![menus.py](documentation/pep8/menus.png)

- constants.py

![constants.py](documentation/pep8/constants.png)

WARNING! I confirm that all my .py files contain last empty line, which might not be rendered or observed on GitHub

### Manual Testing
I performed the following tests. All passed with expected result.

- [x] Validation of week number. Type in strings, negative numbers, floats 
- [x] Validation of weekly sales input. Type in strings, negative numbers, floats
- [x] Display tabular data. Checked for sales, stocks, deliveries, orders. The data conform with the google spreadsheet
- [x] Display tabular data, time period. Data displayed from exactly the chosen week to the end of year 
- [x] Sales forecast after weekly sales input. Calculation results checked, update of the sales worksheet checked
- [x] Forward stocks plan update after weekly sales input. Calculation results checked, update of the stocks worksheet checked 
- [x] Orders recommendation check. Orders calculated correctly, update of the orders worksheet checked
- [x] Deliveries Plan update. Deliveries conform with orders, update of the deliveries worksheet checked
- [x] Forward stock plan update after orders change. Calculation results checked, update of the stocks worksheet checked
- [x] Big sales spikes check. No negative stocks confirmed. Leads to 0 stocks for a while until an updated order results in respective delivery.
- [x] Beginning of a year check. No issues arise with calculating retrospective sales
- [x] End of year check, sales forecasts. No issues arise related to out of boundary iteration.
- [x] End of year check, orders. Orders continue to be planned even when deliveries are expected to arrive outside the period
- [x] Glossary terminal print out check. Pages are turned by hitting enter, return to the main menu confirmed
- [x] Navigating menus checked. Clear of terminal checked

### Bugs

1. _urllib3 2.0 issue on macOS_

When I tried to get data from my google sheet and print out for the first time my terminal returned the warning 
```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, 
currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. 
See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn
``` 
This issue is known to occur with the system Python on macOS, where the SSL module is compiled with LibreSSL instead of OpenSSL. The removal of LibreSSL support in urllib3 version 2.0 means that it cannot be used with the system Python on macOS that is compiled with LibreSSL. 
[urllib3 on GitHub](https://github.com/urllib3/urllib3/issues/3020)

The warning itself does not prevent the code from running, but it indicates that the urllib3 package may not function correctly due to the SSL incompatibility. 

Solution:
  - Install Homebrew
  - Install OpenSSL
  - Install pyenv
  - Configure Zsh for pyenv on macOS [pyenv GitHub](https://github.com/pyenv/pyenv/issues/2136)
  - Set environment variables to point to the correct version of OpenSSL
    [use_homebrew_openssl() function](https://github.com/pyenv/pyenv/blob/master/plugins/python-build/bin/python-build)
  - Install Python with OpenSSL support. In my case it was Python 3.11.7

2. _Validation bug in Input Weekly Sales_

I discovered during testing that the weekly sales input worked incorrectly. When typing in negative numbers the validation scheme seemed to work fine: `While True` loop with `try` and `else` setting displayed the warning, then the correct prompt to input again the same item appeared. And it did not pass to the next item until the correct type value was keyed in. 

However, when checked in the google sheet after an automated worksheet update, I found that all data including the negative numbers were actually stored to the spreadsheet shifting the cells down. Meaning all the values typed in to the input prompt including the wrong ones were appended to the list `week_sales` despite the correct manifestations on the terminal screen.

After debugging with Python Tutor I found that there was a flaw in my logic:
```
week_sales.append([amount])
    if amount >= 0:
    break
```
The list `week_sales` was formed outside the `if` condition that checked for negative values. The solution was obvious:
```
    if amount >= 0:
    week_sales.append([amount])
    break
```

3. _PEP8 warning E712_
331: E712 comparison to False should be 'if cond is False

I used incorrect operator to compare a variable to Boolean
`while quit_program == False:` 

The correct usage would be 
`while not quit_program:` or `while quit_program is False`.

4. _IndexError: list assignment index out of range_

```
for k in range(from_index, len(sales_row)):
        stocks_row = []
        if stocks_row[k-1] <= sales_row[k - 1]:
            stocks_row[k] = deliveries_row[k - 1]
        else:
            stocks_row[k] = (
                stocks_row[k - 1]
                + deliveries_row[k - 1]
                - sales_row[k - 1]
            )
```
In the above code snippet I tried to assign value to the variable `stock_row[k]` before `stock_row` has been properly initialized with a length that includes the index `k`. The correct one is:
```
stocks_row = [0]*len(sales_row)
for k in range(from_index, len(sales_row)):

        if stocks_row[k-1] <= sales_row[k - 1]:
            stocks_row[k] = deliveries_row[k - 1]
        else:
            stocks_row[k] = (
                stocks_row[k - 1]
                + deliveries_row[k - 1]
                - sales_row[k - 1]
            )
```
Here the `stocks_row` is assigned the length of sales_row before the `for` loop. Whereas `sales_row` was previously defined as `sales_values[i]`, `sales_values` being a list of lists obtained from the google sheet using __gspread__ module.  

5. _Negative stocks issue_

- The __beginning stock for the current week__ is defined as:

Begin Stock of previous week - Sales of previous week + Deliveries of previous week. 

Once this formula was realized in Python inside the respective loop I discovered that the future stocks might appear negative which was wrong. The function that calculates stocks was modified to include the condition: `if stocks_row[k-1] <= sales_row[k - 1]:`

This checks if future stocks are less or equal than forecasted sales, then the stocks must be equal the value of deliveries for that future week. Thus, when no deliveries are expected for that particular week, the beginning stock of next week will be equal to 0. 

## Deployment




