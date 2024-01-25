# FORWARD STOCK PLAN AUTOMATION

Forward Stock Plan Automation is a Python terminal program, which is designed to aid to logistic and supply function of distribution and wholesaling companies in order to manage their stock levels and place timely orders. This business process is an everyday job if a distributor strives to avoid out-of-stock situations. An automation of the process becomes a must-have tool for importers, distributors and wholesalers

![Mock screens of the application deployed via Heroku](documentation/mock-screens-heroku.png)

## Business Context
Once there is always a non-zero time between placing an order and a delivery of an item the inbound logistics of any business will face a problem of proper stocks control. Such time of the goods in transit is usually called by distributors "__a lead time__". The problem becomes an essential challenge for a business when marketing cycle of that business is comparable to lead times and sometimes may take more then one week, or several weeks or sometimes even more than a month (take the imports from China for example)

I developed this program aiming at automation of this process for mid-size and smaller businesses that cannot afford the expensive software and try to cope with the task by means of a mere Excel.

A Python-based system can offer significant advantages over a purely Excel-based system in terms of data handling, integration with other systems, customization, and scalability. Python can automate mundane tasks, making them much more efficient. This is particularly useful for tasks such as updating sales forecasts, calculating order recommendations, and controlling stock levels. Automation can reduce the risk of human error, increase efficiency, and free up time for more strategic tasks.

In contrast, while Excel is a great tool for basic data analysis and can be quick and easy to use, it may not be as efficient or effective for larger datasets, complex analytics, and automation. Excel also lacks the integration capabilities of Python, making it less suitable for businesses that need to integrate their logistics systems with other systems.

Basically, what the program does can be briefly described as follows:

- updates weekly sales forecasts based on actual sales input and retrospective sales
- calculates forward stock plan (future stocks) at the beginning of every coming week to the end of a year and based on existing delivery schedule
- calculates orders recommendations for quantity and placement time
- updates forward stock plan after any change to orders, deliveries or sales plans

Planters

Ritter


