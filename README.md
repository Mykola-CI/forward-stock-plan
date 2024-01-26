# FORWARD STOCK PLAN AUTOMATION

Forward Stock Plan Automation is a Python terminal program, which is designed to aid to logistic and supply function of distribution and wholesaling companies in order to manage their stock levels and place timely orders. This business process is an everyday job if a distributor strives to avoid out-of-stock situations. An automation of the process becomes a must-have tool for importers, distributors and wholesalers

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
W--->TD[(Table Data displayed in terminal:<br> Rows-week numbers / Columns- Product Items)]
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
## Future features

- Allow user to change Safety Margin and Minimum Stock level Constants in terminal window.

Currently it may be done relatively easy by a software programmer making changes to dedicated file 'constants.py'

- Allow user to update sales forecasts manually for all desired weeks for a particular item apart from automated sales forecast calculation

Currently it can be done manually by typing in sales for one column/week at a time. User must be given option for multiple input by row, i.e. by product item for multiple weeks in one go

- Allow user to input actual stocks on a weekly basis to account for discrepancies between planned and actual deliveries and shortages/surplus 