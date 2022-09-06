CREATE TABLE "fact_order_accumulating" (
  "order_date_id" int,
  "invoice_date_id" int,
  "payment_date_id" int,
  "customer_id" int,
  "order_number" varchar,
  "invoice_number" varchar,
  "payment_number" varchar,
  "total_order_quantity" int,
  "total_order_usd_amount" decimal,
  "order_to_invoice_lag_days" int,
  "invoice_to_payment_lag_days" int
);

CREATE TABLE "dim_date" (
  "id" int PRIMARY KEY,
  "date" date,
  "month" int,
  "quater_of_year" int,
  "year" int,
  "is_weekend" boolean
);

CREATE TABLE "dim_customer" (
  "id" int PRIMARY KEY,
  "name" varchar
);

ALTER TABLE "fact_order_accumulating" ADD FOREIGN KEY ("order_date_id")  REFERENCES "dim_date" ("id");

ALTER TABLE "fact_order_accumulating" ADD FOREIGN KEY ("invoice_date_id") REFERENCES "dim_date" ("id");

ALTER TABLE "fact_order_accumulating" ADD FOREIGN KEY ("payment_date_id") REFERENCES "dim_date" ("id");

ALTER TABLE "fact_order_accumulating"  ADD FOREIGN KEY ("customer_id")  REFERENCES "dim_customer" ("id");
