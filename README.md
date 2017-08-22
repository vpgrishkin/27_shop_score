# Shop Score Page

The program allows you to monitor online store KPI. The main indicator: waiting time for processing requests.  There are the status colors:
1. Green - the waiting time is less than 7 minutes.
2. Yellow - waiting time from 7 to 30 minutes.
3. Red - waiting time is more than 30 minutes.

Additional indicators:
- number of unprocessed orders;
- number of orders processed for the current day.

The information is refreshed every 10 minutes.

# How to use

## The example on Heroku

[You can see the example on Heroku](https://boiling-shore-98332.herokuapp.com)

## Install virtual envaroment and requirements

``` #!bash

virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

## Set the database connection parameter

### Unix
``` #!bash

DB_CONFIG = 'host={host} dbname={dbname} port={port} user={user} password={password}'
```

You should fill in:
- `{host}` – database host address (defaults to UNIX socket if not provided);
- `{dbname}` – the database name (database is a deprecated alias);
- `{port}` – connection port number (defaults to 5432 if not provided); 
- `{user}` – a user name;
- `{password}` – a password.

### Windows
``` #!bash

SET DB_CONFIG = 'host={host} dbname={dbname} port={port} user={user} password={password}'
```

## Run local sever

``` #!bash

python server.py
```

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
