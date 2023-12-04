CREATE DOMAIN ZIP_CODE_DOMAIN AS CHAR(5) CHECK (VALUE ~ '[0-9]{5}');

CREATE TYPE ADDRESS_TYPE AS (
  street_address VARCHAR(50),
  apartment_unit VARCHAR(8),
  city VARCHAR(50),
  state VARCHAR(50),
  zip_code ZIP_CODE_DOMAIN,
  country VARCHAR(50)
);

ALTER TABLE customers
ADD COLUMN address_details ADDRESS_TYPE;

ALTER TABLE employees
ADD COLUMN address_details ADDRESS_TYPE;

ALTER TABLE authors
ADD COLUMN address_details ADDRESS_TYPE;

ALTER TABLE employees DROP COLUMN address;

ALTER TABLE customers DROP COLUMN address;

UPDATE customers
SET address_details = ROW(
    '281 Saint Nicholas Avenue',
    'Apt 34',
    'New York',
    'New York',
    '10027',
    'United States'
  )
WHERE user_id = '2f96fa528baa4521925ccfcbcf2d325a';

UPDATE customers
SET address_details = ROW(
    '350 W 110th St',
    'Apt 24',
    'New York',
    'New York',
    '10025',
    'United States'
  )
WHERE user_id = '518e6071499142f19ac38843af0f2454';

UPDATE customers
SET address_details = ROW(
    'Broadway 116th St',
    'Apt 44',
    'New York',
    'New York',
    '10023',
    'United States'
  )
WHERE user_id = '77b9b181ee4b4057b99876995cf45fa2';

UPDATE customers
SET address_details = ROW(
    '414 W 120th St',
    'Apt 11',
    'New York',
    'New York',
    '10027',
    'United States'
  )
WHERE user_id = '7ca423fcba164376b4df624b7c5cfc41';

UPDATE customers
SET address_details = ROW(
    '285 Saint Nicholas Avenue',
    'Apt 62',
    'New York',
    'New York',
    '10027',
    'United States'
  )
WHERE user_id = 'b289a1587833451ea2246fcb9ca1f2b9';

UPDATE customers
SET address_details = ROW(
    '285 Saint Nicholas Avenue',
    'Apt 54',
    'New York',
    'New York',
    '10027',
    'United States'
  )
WHERE user_id = 'da2aea9ed14a410abf84de9d758b55c5';

UPDATE employees
SET address_details = ROW(
    '132 Apple St',
    'Apt 2',
    'New York',
    'New York',
    '10001',
    'USA'
  )
WHERE user_id = 'ebd446b53f494bf9a32eb3ef0d12e6a5';

UPDATE employees
SET address_details = ROW(
    '789 Cedar Ln.',
    'Apt 10',
    'Queens',
    'New York',
    '11301',
    'USA'
  )
WHERE user_id = 'fa0386f7ce0c4a8dab0e23dd0a26663b';

UPDATE employees
SET address_details = ROW(
    '456 Birch Ave.',
    'Apt 587',
    'Brooklyn',
    'New York',
    '11201',
    'USA'
  )
WHERE user_id = 'd6ae693fc86e41699291bd79b4c91770';

UPDATE employees
SET address_details = ROW(
    '101 Dogwood Dr.',
    'Apt 354',
    'Bronx',
    'New York',
    '10451',
    'USA'
  )
WHERE user_id = 'ad3d1c5347f549c28d5563845e58c7bf';

UPDATE employees
SET address_details = ROW(
    '234 Elm Pl.',
    'Apt 269',
    'Manhattan',
    'New York',
    '10002',
    'USA'
  )
WHERE user_id = 'c3c3512be55e4e93963dc567132bd044';

UPDATE employees
SET address_details = ROW(
    '567 Fir Blvd.',
    'Apt 338',
    'Staten Island',
    'New York',
    '10301',
    'USA'
  )
WHERE user_id = '636291d2312644cca8b1b43e2ac343cb';

UPDATE employees
SET address_details = ROW(
    '890 Grove Ct.',
    'Apt 553',
    'Harlem',
    'New York',
    '10027',
    'USA'
  )
WHERE user_id = '773241f02520479190411817de72b3a4';

UPDATE employees
SET address_details = ROW(
    '456 Ivy Rd.',
    'Apt 806',
    'Flushing',
    'New York',
    '11354',
    'USA'
  )
WHERE user_id = '5e2cc6d12f4542b0b0e05d6514c64187';

UPDATE employees
SET address_details = ROW(
    '123 Holly Way',
    'Apt 415',
    'Astoria',
    'New York',
    '11102',
    'USA'
  )
WHERE user_id = '45024012b06741c3ad8787f8e61d244b';

UPDATE employees
SET address_details = ROW(
    '789 Juniper Sq.',
    'Apt 441',
    'Yonkers',
    'New York',
    '10701',
    'USA'
  )
WHERE user_id = '38441acff27b45ddae36969769c166f4';

UPDATE authors
SET address_details = ROW(
    '744 Oak St',
    'Apt 426',
    'Rochester',
    'New York',
    '12712',
    'USA'
  )
WHERE user_id = '8430a65bea6b4d2a86cbd019a2649bc6';

UPDATE authors
SET address_details = ROW(
    '502 Cedar Rd',
    'Apt 918',
    'Albany',
    'New York',
    '11254',
    'USA'
  )
WHERE user_id = '2bf9531d1c40409eacee6992d19e9e74';

UPDATE authors
SET address_details = ROW(
    '210 Elm Rd',
    'Apt 323',
    'Queens',
    'New York',
    '12211',
    'USA'
  )
WHERE user_id = 'f0d3072a19604f19bc8c4b38f7a83769';

UPDATE authors
SET address_details = ROW(
    '191 Elm Rd',
    'Apt 316',
    'Rochester',
    'New York',
    '10385',
    'USA'
  )
WHERE user_id = '4c9ca6fd33cd47b887965d07a46512cd';

UPDATE authors
SET address_details = ROW(
    '338 Cedar Ave',
    'Apt 523',
    'New York',
    'New York',
    '12468',
    'USA'
  )
WHERE user_id = 'fd5f2ad39b544a4fac7e3bafb16e8419';

UPDATE authors
SET address_details = ROW(
    '668 Cedar Blvd',
    'Apt 184',
    'Bronx',
    'New York',
    '11727',
    'USA'
  )
WHERE user_id = '7392d1094a8f4db386b9368695a6c84b';

UPDATE authors
SET address_details = ROW(
    '332 Elm Blvd',
    'Apt 572',
    'Queens',
    'New York',
    '10499',
    'USA'
  )
WHERE user_id = '3d6445f74c5246ff81946e7b6129ea3b';

UPDATE authors
SET address_details = ROW(
    '595 Pine Rd',
    'Apt 948',
    'Albany',
    'New York',
    '13983',
    'USA'
  )
WHERE user_id = 'd8b2be5f480e44b086462d8d8bb95e57';

ALTER TABLE Employees
ALTER COLUMN address_details
SET NOT NULL;