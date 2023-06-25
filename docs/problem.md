# Problem Statement

## Background
The application works by comparing live prices (in a table “live_prices”) of
goods against a pre-computed maximum purchase price (in a table
“goods_max_price”), if the live price is below the max price for that goods
record it will generate an opportunity into another database table
(“app_output”). We can assume the live price data will be coming in from third
parties through a separate API into the database table at a rate of 50,000
products per hour at the peak.

## Basic use cases

1. A database configuration file should be read by the application upon
    starting e.g. containing the values required for the connection string.

2. The application will behave as mentioned in the background section;
    comparing the live price to the max price and generating an output
    record if necessary. The output record should include the fields:
    created_timestamp, uuid, max_price.

3. The application should be "always on" and continuously or routinely
    check for new data in the live_prices table, which can be populated with
    fresh data at any time.

4. The application should move the live price data to an archive table
    (“live_price_archive”) once that goods record has been considered.

5. This application should have a well-thought-out architecture as there
    will be changes in the future when the business logic grows to be more
    complex than simply “live_price < max_price”.
