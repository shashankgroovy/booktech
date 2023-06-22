BookTech Application – v1.1
---------------------------

Background
-----------
The application works by comparing live prices (in a table “live_prices”)
of goods against a pre-computed maximum purchase price (in a table
“goods_max_price”), if the live price is below the max price for
that goods record it will generate an opportunity into another
database table (“app_output”). The live price data will be coming
in from third parties through a separate API into the database
table at a rate of 50,000 products per hour at the peak.

Task
----
You are going to create the application from scratch, in Java/Python, it is
not necessary to containerize the application at this point. You will be
provided some sample data which you should ingest (ideally mysql or
postgresql) and do a quick profile of the data.

Requirements
============

1. Produce a data dictionary for the sample data.
2. A database configuration file should be read by the application upon
    starting e.g. containing the values required for the connection string.
3. The application will behave as mentioned in the background section;
    comparing the live price to the max price and generating an output
    record if necessary. The output record should include the fields:
    created_timestamp, uuid, max_price.
4. The application should be "always on" and continuously or routinely
    check for new data in the live_prices table, which can be populated with
    fresh data at any time.
5. The application should move the live price data to an archive table
    (“live_price_archive”) once that goods record has been considered.
6. This application should have a well-thought-out architecture as there
    will be changes in the future when the business logic grows to be more
    complex than simply “live_price < max_price”.
7. You will return a zip file containing:
    a. Code files
    b. README file with instructions on how to run the application
    c. A copy of the app_output table with the data your application
    produced from the sample data
    d. Anything else you think is required to run the application
