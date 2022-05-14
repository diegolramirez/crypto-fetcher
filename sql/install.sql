CREATE TABLE public.coin_data (
	coin varchar NOT NULL,
	"date" date NOT NULL,
	price float8 NULL,
	"json" json NULL,
	insert_ts timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT coin_data_pkey PRIMARY KEY (coin, date)
);

CREATE TABLE public.coin_month_data (
	coin varchar NOT NULL,
	"year" int4 NOT NULL,
	"month" int4 NOT NULL,
	min_price float8 NULL,
	max_price float8 NULL,
	CONSTRAINT coin_month_data_pkey PRIMARY KEY (coin, year, month)
);
