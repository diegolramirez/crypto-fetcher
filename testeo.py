from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv

engine = create_engine(
            f"postgresql+psycopg2://{os.environ['PG_USERNAME']}:{os.environ['PG_PASSWORD']}@localhost:{os.environ['PG_PORT']}/{os.environ['PG_DB']}"
        )

from sql.queries import queries
# with engine.connect() as con:

#     # rs = con.execute('SELECT * FROM coin_data')
#     rs = con.execute('SELECT * FROM pg_catalog.pg_tables;')
#     # print(rs.all())

#     for row in rs:
#         print(row)


print(queries)

# print(queries())



# 0 3 * * * python3 crypto_fetcher.py -c bitcoin --save-db
# 0 3 * * * python3 crypto_fetcher.py -c ethereum --save-db
# 0 3 * * * python3 crypto_fetcher.py -c cardano --save-db