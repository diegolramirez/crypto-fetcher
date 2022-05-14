# crypto_fetcher

## Overview

Technical assessment for the Data Engineering Technical Lead position at [Mutt](https://muttdata.ai/) presented by [Diegol Ramírez-Milano](https://github.com/diegolramirez).

The actual technical assessment questions are under the `/assessments` folder  

## Name

crypto_fetcher

## Description

Fetches a cryptocurrency price from [CoinGecko API](https://www.coingecko.com/en/api/documentation). Receives as parameters the coin name and date to fetch.

## Prerequisites

This applications assumes the following are installed

- Python 3.8.0+ under the command `python`
- Python pip under the command `pip`
- Python virtualenv
- Docker

## Installation

Create a `.env` file using the following template, change any field as desired

```.env:
PG_USERNAME=not_postgres
PG_PASSWORD=my_strong_password
PG_DB=crypto
PG_PORT=5432
CONTAINER_NAME=postgres-1
```

Afterwards run the script `setup.sh` as follows:

```bash:
bash setup.sh
```

This script install the required Python packages and spins-up a Docker container with a PostgreSQL DataBase to store the retrieved data.

## Usage

Run the Python script and pass the required arguments as follows:

```bash:
python crypto_fetcher.py --coin bitcoin
```

To view the full list of arguments run the command

```bash:
python crypto_fetcher.py --help
```

All results are stored locally under the directory `/data`. If argument `--save-db` is passed then results are also stored in the PostgreSQL database. The full logs of the application can be found inside the file `logs/crypto.log` which is created after the first execution.

## Crontab

Currently there are 3 processes running under the crontab as follows:

```bash:
0 3 * * * python crypto_fetcher.py -c bitcoin --save-db
0 3 * * * python crypto_fetcher.py -c cardano --save-db
0 3 * * * python crypto_fetcher.py -c ethereum --save-db
```

These processes run daily at 03:00 to fetch the data for 3 different cryptocurrencies: bitcoin, cardano and ethereum. To access the list of processes in the crontab run the command `crontab -e`.

## SQL

The queries for question #3 can be found under the directory `sql/` with the names `script3-1.sql` and `script3-2.sql`

## Support

[Contact me via email](mailto:diegolramirezmilano@gmail.com)
