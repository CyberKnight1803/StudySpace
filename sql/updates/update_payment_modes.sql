CREATE TYPE PAYMENT_DETAILS AS ENUM(
  'Apple pay',
  'Google pay',
  'Credit card',
  'Debit card'
);

ALTER TABLE customers
ALTER COLUMN payment_details TYPE PAYMENT_DETAILS USING payment_details::PAYMENT_DETAILS;

ALTER TABLE customers DROP CONSTRAINT customers_payment_details_check;