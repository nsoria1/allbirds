# Allbirds

## Programming assignment

### How to run it?

- It is a requirement to have docker install in your computer.
- Place any file you want to process on the spec and data folders
- Run `docker compose up -d` at the root of the repository.

### How to run unit tests? 
If you have the `requirements.txt` file packages installed in your local, you can run python `tests.py` to run some basics test on the classes.

## SQL assignment

Report on quantity sold by month and product_type. Order sale date is in the " created_at_pacific_timestamp" column. 
```sql
select
	to_char(o.created_at_pacific_timestamp, 'YYYYMM') as year_month,
	s.product_type,
	sum(ol.quantity) as qty
from orders o
inner join order_line_items ol on o.id = ol.order_id
inner join skus s on ol.sku = s.sku
group by 1, 2
```

List email addresses of customers that ordered Runners before the first time they ordered Loungers. 
```sql
with cte as (
	select 
		o.email, 
		s.product_type, 
		o.created_at_pacific_timestamp, 
		row_number() over (partition by o.email order by o.created_at_pacific_timestamp asc) as row_num,
		lead(s.product_type, 1) over (partition by o.email order by o.created_at_pacific_timestamp asc) as next_product_type
	from orders o
	inner join order_line_items ol on o.id = ol.order_id
	inner join skus s on ol.sku = s.sku
)
select email
from cte
where row_num = 1 and product_type = 'Runners' and next_product_type = 'Loungers'
```

List email addresses that ordered Runners twice before the first time they ordered Loungers. 
```sql
with cte as (
	select 
		o.email, 
		s.product_type, 
		o.created_at_pacific_timestamp, 
		row_number() over (partition by o.email order by o.created_at_pacific_timestamp asc) as row_num,
		lead(s.product_type, 1) over (partition by o.email order by o.created_at_pacific_timestamp asc) as next_product_type,
	from orders o
	inner join order_line_items ol on o.id = ol.order_id
	inner join skus s on ol.sku = s.sku
)
select email
from cte
where (row_num = 1 and product_type = 'Runners' and next_product_type = 'Runners')
and (row_num = 2 and product_type = 'Runners' and next_product_type = 'Loungers')
```

List of customers emails and its highest product price whose last order was 5 days ago.
```sql
select 
	o.email, 
	max(ol.price) as max_price
from orders o
inner join order_line_items ol on o.id = ol.order_id
inner join skus s on ol.sku = s.sku
where o.created_at_pacific_timestamp::date = current_date - INTERVAL '5 DAYS'
group by 1; 
```

Since question #2 and #3 are similar. Do you know any tool, framework or way to create a generic way to resolve this problem? For example dbt, PLSQL, etc.
Not 100% sure but you could use in a dbt package, the helpers to iterate in a collection to automate the new filters on where
It could be something like the following approach:
```sql
{% set var numbers=(1, 2, 3) %}
  with cte as (
    ...
  )
  select
    ...
  from
    ...
  where  
{%- for num in numbers %}
    (row_num = '{{ num }}' and product_type = 'Runners' and next_product_type = 'Runners') 
    {%- if not loop.last %},{% endif -%}
{%- endfor %}
```
It also can be done with python by adding an N amount of rows to the sql query to materialize the results.

How (if at all) would you change this schema to better support queries of this kind?
If the schema is used by the application, I would not change the schema. Instead, I'll model the data as required in the warehouse.
I would do a wide table by joining all in one to avoid join computation. In the pipeline, I would be able to create an aggregated accumulator table for the n counts required.
