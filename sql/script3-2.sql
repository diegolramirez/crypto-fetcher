with
	last_date as (
	select
		cd.coin,
		cd.date,
		cd.json->'market_data'->'market_cap'->'usd' as market_cap
	
	from
		coin_data cd
		inner join (
			select
				cd.coin,
				max(cd.date) as last_date
			
			from 
				coin_data cd
			
			group by
				cd.coin
			) as ld on ld.coin = cd.coin and ld.last_date = cd.date
	),
	
	condicion as (
	select 
		cd.coin,
		cd.date,
		cd.price,
		case
			when
				lag(cd.price,3) over(partition by cd.coin order by cd.date asc) < lag(cd.price,4) over(partition by cd.coin order by cd.date asc)	
				and
				lag(cd.price,2) over(partition by cd.coin order by cd.date asc) < lag(cd.price,3) over(partition by cd.coin order by cd.date asc)	
				and 
				lag(cd.price,1) over(partition by cd.coin order by cd.date asc) < lag(cd.price,2) over(partition by cd.coin order by cd.date asc)
				and 
				cd.price > lag(cd.price,1) over(partition by cd.coin order by cd.date asc)
				
				then 1
			else 0
		end as estado
	
	from 
		coin_data cd
	),
	
	price_up as (
	select
		c.coin,
		c.date,
		c.price,
		c.estado,
		case
			when
				c.estado = 1 then c.price - lag(c.price,1) over(partition by c.coin order by c.date asc) 
			else null
		end as price_diff
	
	from
		condicion c
	),
	
	average_price as (
	select
		pu.coin,
		avg(pu.price_diff) as avg_price_increase
	
	from
		price_up pu
	
	group by pu.coin
	),
	
	result as (
	select
		ap.coin,
		ap.avg_price_increase,
		ld.market_cap
	
	from
		average_price ap
		inner join last_date ld on ld.coin = ap.coin
	)

select * from result