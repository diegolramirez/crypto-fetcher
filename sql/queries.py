queries = {
    "insert_coin_data": """
    insert into coin_data(coin, date, price, json)
    values(:coin, :date, :price, :json)
    on conflict do nothing;""",
    "update_coin_month_data": """
    insert into coin_month_data 
	select
		:coin as coin,
		:year as year,
		:month as month,
		min(cd.price) as min_price,
		max(cd.price) as max_price
	from
		coin_data as cd
	where
		coin = :coin
		and extract(year from cd.date) = :year
		and extract(month from cd.date) = :month
    on conflict (coin, year, month) do update set
        min_price = excluded.min_price, 
        max_price = excluded.max_price;"""
    }
