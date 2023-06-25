# Generated app output

Booktech app processes opportunities and any valid opportunities are kept in
`app_output` table.

## Schema

The schema of the generated app output table is pretty straight forward.
For each opportunity we are tracking both the max_price and live_price.

 ```
postgres=# \d app_output ;
                         Table "public.app_output"
   Column   |            Type             | Collation | Nullable | Default
------------+-----------------------------+-----------+----------+---------
 uuid       | uuid                        |           |          |
 max_price  | numeric                     |           |          |
 live_price | numeric                     |           |          |
 created_at | timestamp without time zone |           |          |
 ```

## Output

Now let's look at some of the entries. Based on the output we can see that new
opportunities based on the core logic where live_price > max_price.

```
postgres=# select * from app_output limit 20;
                 uuid                 | max_price | live_price |     created_at
--------------------------------------+-----------+------------+---------------------
 d93601ac-1254-492b-aeff-fab464fc1f0b |     14.26 |      26.79 | 2023-06-25 02:11:07
 e9279fb0-979b-4f64-9077-4fbb9adeb02c |     13.78 |       28.9 | 2023-06-25 02:11:07
 c5130c65-5930-468f-9276-899ec09e915c |      6.64 |     118.19 | 2023-06-25 02:11:07
 f830b6fc-5cd5-40d6-be20-8f71b5b6b58a |     20.71 |      47.59 | 2023-06-25 02:11:07
 05644bd8-e0e3-4aa1-9d4f-9b6dfe0bfc5b |       2.8 |      62.09 | 2023-06-25 02:11:07
 09b07dd1-aa20-4459-a5ff-16ffc874bf62 |     53.57 |      80.79 | 2023-06-25 02:11:07
 b27e7e10-65d7-4194-bfad-ad66196faa78 |      5.15 |      24.29 | 2023-06-25 02:11:07
 13f5a797-6092-4a93-8ff1-382738c4c846 |     44.64 |      49.59 | 2023-06-25 02:11:07
 8c3c36b1-084b-4bf5-bc96-044a00fd5e08 |      8.02 |      40.59 | 2023-06-25 02:11:07
 3bc0d237-33ce-4f41-939c-f422c9554d18 |     13.84 |      22.29 | 2023-06-25 02:11:08
```

We can find a full csv file which completely processed data in the `data/`
directory with the name `app_output.csv`

[Link to file](./data/app_output.csv)

And that's about it!
