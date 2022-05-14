from argparse import ArgumentParser
from datetime import date, datetime
import json
import requests
from dataclasses import dataclass, field
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sql.queries import queries
import logging
import os
from dotenv import load_dotenv

log = logging.getLogger(__name__)
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("logs/crypto.log"), logging.StreamHandler()],
)


# TODO: add multiprocessing
# TODO: create crontab
@dataclass(frozen=True, order=True)
class ExamDate:
    sort_index: int = field(init=False, repr=False)
    input_date: str = field(default=date.today().isoformat(), repr=False)
    date_: date = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "date_", datetime.strptime(self.input_date, "%Y-%m-%d").date()
        )
        object.__setattr__(self, "sort_index", self.date_.toordinal())

    def iso_str(self) -> str:
        return self.date_.isoformat()

    def coingecko_str(self) -> str:
        return self.date_.strftime("%d-%m-%Y")


def argument_parser():
    my_parser = ArgumentParser(
        description=(
            "Retrieves a cryptocurrency data from coingecko API"
            "To see more visit https://www.coingecko.com/en/api/documentation"
            "Receives the coin name and a date as arguments"
        )
    )
    my_parser.add_argument(
        "-c",
        "--coin",
        action="store",
        choices=["bitcoin", "cardano", "ethereum"],
        required=True,
        help="REQUIRED - Set the coin to be fetched",
    )
    my_parser.add_argument(
        "-s",
        "--start-date",
        action="store",
        type=ExamDate,
        default=ExamDate(),
        help="OPTIONAL - Set the date to fetch data from. Default is today's date",
    )
    my_parser.add_argument(
        "-e",
        "--end-date",
        action="store",
        type=ExamDate,
        help="OPTIONAL - Set the end date to fetch data from",
    )
    my_parser.add_argument(
        "--save-db",
        action="store_true",
        help="OPTIONAL - Sets if the data is stored in the db. Default is false",
    )
    args = vars(my_parser.parse_args())

    if args["start_date"] > ExamDate():
        raise my_parser.error("Start date cannot be in the future!")
    if args["end_date"] is not None and args["end_date"] > ExamDate():
        raise my_parser.error("End date cannot be in the future!")
    if args["end_date"] is not None and args["end_date"] < args["start_date"]:
        raise my_parser.error("End date must be equal or greater than start date")

    log.info(f"Received arguments: {args}")

    return args


def fetch_coin(coin: str, fetch_date: ExamDate) -> dict:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/history?date={fetch_date.coingecko_str()}"
    log.info(f"Fetching CoinGecko API at {url}")
    res = requests.get(url)
    log.info("Response obtained from CoinGecko")
    return res.json()


def save_data(
    coin: str, fetch_date: ExamDate, data: dict, save_db: bool = False
) -> None:
    log.info("Saving data")
    path = f"./data/{coin}_{fetch_date.iso_str()}.json"
    with open(path, "w") as outfile:
        json.dump(data, outfile)
    log.info(f"Data saved locally to {path}")
    if save_db:
        engine = create_engine(
            f"postgresql+psycopg2://{os.environ['PG_USERNAME']}:{os.environ['PG_PASSWORD']}@localhost:{os.environ['PG_PORT']}/{os.environ['PG_DB']}"
        )
        with engine.connect() as con:
            insert_data = {
                "coin": coin,
                "date": fetch_date.iso_str(),
                "price": data["market_data"]["current_price"]["usd"],
                "json": json.dumps(data),
            }
            insert_sql = text(queries["insert_coin_data"])
            con.execute(insert_sql, **insert_data)
            log.info("Data saved to db, table 'coin_data'")
            update_data = {
                "coin": coin,
                "year": fetch_date.date_.year,
                "month": fetch_date.date_.month,
            }
            update_sql = text(queries["update_coin_month_data"])
            con.execute(update_sql, **update_data)
            log.info("Prices updated in db, table 'coin_month_data'")


def fetch_save(coin: str, fetch_date: ExamDate, save_db: bool = False) -> None:
    response = fetch_coin(coin, fetch_date)
    save_data(coin, fetch_date, response, save_db)


def main() -> None:
    log.info("Loading .env")
    load_dotenv()
    arguments = argument_parser()
    coin, start_date, end_date, save_db = arguments.values()
    end_date = ExamDate(start_date.iso_str()) if end_date is None else end_date

    dates_range = [
        ExamDate(date.fromordinal(i).isoformat())
        for i in range(start_date.date_.toordinal(), end_date.date_.toordinal() + 1)
    ]

    for fetch_date in dates_range:
        log.info(f"Processing date {fetch_date.iso_str()}")
        try:
            # response = fetch_coin(coin, fetch_date)
            # save_data(coin, fetch_date, response, save_db)
            fetch_save(coin, fetch_date, save_db)
        except Exception as e:
            log.error(f"Could not process given date, skipping it. Error: {str(e)}")
        else:
            log.info("Date processed successfully")
    log.info("Done :)")


if __name__ == "__main__":
    main()
