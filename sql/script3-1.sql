select
	cd.coin,
	extract(year from cd.date) as "year",
	extract(month from cd.date) as "month",
	avg(cd.price) as avg_price,
	min(cd.price) as min_price,
	max(cd.price) as max_price
from
	coin_data as cd
group by
	1,2,3