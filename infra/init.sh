#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    drop table if exists orders;
    drop table if exists skus;
    drop table if exists order_line_items;
	CREATE TABLE orders (id CHARACTER VARYING(19) NOT NULL PRIMARY KEY, email CHARACTER VARYING(255),  created_at_pacific_timestamp TIMESTAMP WITHOUT TIME ZONE); 
    CREATE TABLE skus (sku CHARACTER VARYING (50) NOT NULL PRIMARY KEY, product_type CHARACTER VARYING (255) NOT NULL, product_name CHARACTER VARYING (255) NOT NULL, size CHARACTER VARYING (50), color_name CHARACTER VARYING (255), color_hex CHARACTER VARYING (50));
    CREATE TABLE order_line_items ( order_id CHARACTER VARYING(19) NOT NULL REFERENCES orders  ON DELETE CASCADE, order_line_number INTEGER NOT NULL, quantity INTEGER NOT NULL, price DECIMAL(12,2) NOT NULL, sku CHARACTER VARYING(20) NOT NULL REFERENCES skus ON DELETE RESTRICT, PRIMARY KEY (order_id, order_line_number));
EOSQL