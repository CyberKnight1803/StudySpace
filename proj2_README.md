# Project 2

## Team

1. Omkar Vijay Pitale : **op2281**
2. Akshay Ganesh Iyer: **agi2108**
3. Prahlad Koratamaddi: **TA Mentor** 

### Database

PostgreSQL account: **op2281**

# Advanced Features

## Text Attribute

1. Book Search new attribute needed / Customer bio search / Author bio
    
    ```sql
    ALTER TABLE subscriptions
    ALTER COLUMN description TYPE text;
    
    ALTER TABLE Books
    ALTER COLUMN description TYPE text;
    ```
    
    There is not much substantial change when the description for subscriptions is changed from `VARCHAR` to `TEXT` but altering the type for descriptions in books to `TEXT` will help in the search features which is our mean feature of our product **StudySpace**.
    
    This will help in implementing full text search features supported by PostgreSQL.
    

1. Author Bio, new text attribute 
    
    Enabling Authors to add BIO in their profile will help customer to search for authors based on their interests which helps in letting them know what these authors books are.. 
    
    ```sql
    ALTER TABLE Authors 
    ADD COLUMN bio text;
    ```
    
    Added rows with new bios for each author.
    

## Custom Type

1. Update `payment_details` type 
    
    We decided to updated payment_details because in future if we need to add more payment modes, the previous approach might not be feasible. `ENUM` simplifies this problem. 
    
    [This was also the feedback from our mentor]. 
    
    ```sql
    CREATE TYPE PAYMENT_DETAILS AS ENUM(
      'Apple pay',
      'Google pay',
      'Credit card',
      'Debit card'
    );
    
    ALTER TABLE customers
    ALTER COLUMN payment_details TYPE PAYMENT_DETAILS USING payment_details::PAYMENT_DETAILS;
    
    ALTER TABLE customers
    DROP CONSTRAINT customers_payment_details_check;
    ```
    
    Since `ENUM` type inherently restricts its values to given list, we need to drop the check constraint we added earlier. 
    
2. Adding `address_detail` attribute as a composite custom type 
    - To make the address given by user entity more structured we define a new composite type, that takes in the street address, apartment unit, city, state, zip code and country.
    - Since custom type does not allow to add constraints and in US, the zip code has 5 digits, so we create a new domain `ZIP_CODE_DOMAIN` for zip code before defining `ADDRESS_TYPE`
    
    ```sql
    CREATE DOMAIN ZIP_CODE_DOMAIN AS CHAR(5)
    CHECK (VALUE ~ '[0-9]{5}');
    
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
    
    ALTER TABLE customers 
    DROP COLUMN address;
    
    ALTER TABLE employees 
    ADD COLUMN address_details ADDRESS_TYPE;
    
    ALTER TABLE employees 
    DROP COLUMN address;
    
    ALTER TABLE authors 
    ADD COLUMN address_details ADDRESS_TYPE;
    ```
    
    Authors don’t have an address field, so a new feature for authors!
    
    After updating the data (using `UPDATE` queries) as per the new type, we add the `NOT NULL` constraint for employees address to make sure our schema goes by original ER constraints modeled.
    
    ```sql
    ALTER TABLE Employees 
    ALTER COLUMN address_details SET NOT NULL;
    ```
    

## Triggers

### 1. Enforcing Total Participation Constraint of Books in relationship between Books and Sections

**********Logic for trigger for********** `classified_by` **********table**********

1. In case of `DELETE` 
    1. If not deleted from `books` then insert back the old row and raise exception for violating total participation constraint.
2. In case of `UPDATE`
    1. If old `book_id` has 0 entries in `classified_by` then raise exception for violating total participation constraint.
3. In case of `INSERT`
    1. Cannot insert without book present in books table because of foreign key constraint. So already handled.

```sql
CREATE FUNCTION checkBookSectionParticipationInClassified_by()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'DELETE' THEN 
        IF (
            SELECT COUNT(*)
            FROM Classified_by C 
            WHERE C.book_id = OLD.book_id
        ) = 0 AND (
            SELECT COUNT(*)
            FROM Books B 
            WHERE B.book_id = OLD.book_id
        ) = 1 THEN
    
                INSERT INTO Classified_by(
                    book_id, 
                    section_id
                ) VALUES (
                    OLD.book_id, 
                    OLD.section_id
                );
            
             RAISE EXCEPTION 'Total Participation Constraint Violation';     
        END IF;
    
    ELSIF TG_OP = 'UPDATE' THEN 
        IF (
            SELECT COUNT(*)
            FROM Classified_by C 
            WHERE C.book_id = OLD.book_id
        ) = 0 THEN 
            
            RAISE EXCEPTION 'Total Participation Constraint Violation';       
        
        END IF;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql
```

```sql
CREATE CONSTRAINT TRIGGER BookSectionTotalParticipationTrigger
AFTER UPDATE OR DELETE ON Classified_by 
DEFERRABLE INITIALLY DEFERRED 
FOR EACH ROW 
EXECUTE FUNCTION checkBookSectionParticipationInClassified_by();
```

**********Logic for trigger for********** `books` **********table**********

1. In case of `INSERT` 
    1. If no entry in `classified_by` then delete and raise exception for violating total participation constraint
2. In case of `UPDATE`
    1. If new `book_id` has 0 entries in `classified_by` then raise exception for violating total participation constraint.
3. In case of `DELETE`
    1. Already handled because of on delete cascade.

```sql
CREATE FUNCTION checkBookSectionParticipationInBooks()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN 
        IF (
            SELECT COUNT(*)
            FROM Classified_by C 
            WHERE C.book_id = NEW.book_id
        ) = 0 THEN 
            
            DELETE FROM Books B 
            WHERE B.book_id = NEW.book_id;

            RAISE EXCEPTION 'Total Participation Constraint Violation';
        
        END IF;
    
    ELSIF TG_OP = 'UPDATE' THEN 
        IF (
            SELECT COUNT(*)
            FROM Classified_by C 
            WHERE C.book_id = NEW.book_id
        ) = 0 THEN  

            UPDATE Books B 
            SET B.book_id = OLD.book_id
            WHERE B.book_id = NEW.book_id;
            
            RAISE EXCEPTION 'Total Participation Constraint Violation';
        
        END IF;    
    END IF;    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

```sql
CREATE CONSTRAINT TRIGGER BookSectionTotalParticipationTrigger
AFTER INSERT OR UPDATE ON Books 
DEFERRABLE INITIALLY DEFERRED 
FOR EACH ROW 
EXECUTE FUNCTION checkBookSectionParticipationInBooks();
```

 

### 2. Enforcing Total Participation Constraint of Books in relationship between Books and Authors

Analogous to enforcing total participation constraint of Books in books and sections, we can enforce the total participation 

constraint of books with same reasoning. 

```sql
CREATE FUNCTION checkBookAuthorParticipationInWritten_by()
RETURNS TRIGGER AS $$
BEGIN 
    IF TG_OP = 'DELETE' THEN 
        IF (
            SELECT COUNT(*)
            FROM Written_by W 
            WHERE W.book_id = OLD.book_id
        ) = 0 AND (
            SELECT COUNT(*)
            FROM Books B 
            WHERE B.book_id = OLD.book_id
        ) = 1 THEN
    
                INSERT INTO Written_by(
                    book_id, 
                    author_id
                ) VALUES (
                    OLD.book_id, 
                    OLD.author_id
                );
             RAISE EXCEPTION 'Total Participation Constraint Violation';     
        END IF;
    
    ELSIF TG_OP = 'UPDATE' THEN 
        IF (
            SELECT COUNT(*)
            FROM Written_by W
            WHERE W.book_id = OLD.book_id
        ) = 0 THEN 
            
            RAISE EXCEPTION 'Total Participation Constraint Violation';       
        END IF;
   
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER BookAuthorTotalParticipationTrigger
AFTER UPDATE OR DELETE ON Written_by 
DEFERRABLE INITIALLY DEFERRED 
FOR EACH ROW 
EXECUTE FUNCTION checkBookAuthorParticipationInWritten_by();
```

```sql
CREATE FUNCTION checkBookAuthorParticipationInBooks()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN 
        IF (
            SELECT COUNT(*)
            FROM Written_by W 
            WHERE W.book_id = NEW.book_id
        ) = 0 THEN 
            
            DELETE FROM Books B 
            WHERE B.book_id = NEW.book_id;

            RAISE EXCEPTION 'Total Participation Constraint Violation';
        
        END IF;
    
    ELSIF TG_OP = 'UPDATE' AND TG_TABLE_NAME = '' THEN 
        IF (
            SELECT COUNT(*)
            FROM Written_by W 
            WHERE W.book_id = NEW.book_id
        ) = 0 THEN  

            UPDATE Books B 
            SET B.book_id = OLD.book_id
            WHERE B.book_id = NEW.book_id;
            
            RAISE EXCEPTION 'Total Participation Constraint Violation';
        
        END IF;
    
    END IF; 
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER BookAuthorTotalParticipationTrigger
AFTER INSERT OR UPDATE ON Books 
DEFERRABLE INITIALLY DEFERRED 
FOR EACH ROW 
EXECUTE FUNCTION checkBookAuthorParticipationInBooks();
```

### 3. Non-Overlap Constraint in Child Entities of User (ISA - Hierarchy)

1. `user_id`, `email`, `mobile` should be unique across all child entities i.e. `Customers`, `Employees`, `Authors`

The trigger will be fired when and `INSERT` or `UPDATE` query for `Customers`, `Employees` or `Authors` is executed.

```sql
CREATE OR REPLACE FUNCTION checkUserUniqueness()
RETURNS TRIGGER AS $$ 
DECLARE 
    user_count INT;
BEGIN

		IF TG_OP = 'INSERT' THEN 
	    SELECT COUNT(*) INTO user_count
	    FROM (
	        SELECT user_id 
	        FROM Customers C 
	        WHERE C.user_id = NEW.user_id OR C.email = NEW.email OR C.mobile = NEW.mobile 
	        UNION 
	        SELECT user_id 
	        FROM Employees E 
	        WHERE E.user_id = NEW.user_id OR E.email = NEW.email OR E.mobile = NEW.mobile
	        UNION 
	        SELECT user_id 
	        FROM Authors A 
	        WHERE A.user_id = NEW.user_id OR A.email = NEW.email OR A.mobile = NEW.mobile
	    ) AS U; 
	
	    IF user_count > 0 THEN 
	        RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';
	    END IF;
		
		ELSIF TG_OP = 'UPDATE' AND TG_TABLE_NAME = 'customers' THEN 
			SELECT COUNT(*) INTO user_count
	    FROM (
	        SELECT user_id 
	        FROM Customers C 
	        WHERE (C.email = NEW.email OR C.mobile = NEW.mobile) AND C.user_id != NEW.user_id
	        UNION 
	        SELECT user_id 
	        FROM Employees E 
	        WHERE E.email = NEW.email OR E.mobile = NEW.mobile
	        UNION 
	        SELECT user_id 
	        FROM Authors A 
	        WHERE A.email = NEW.email OR A.mobile = NEW.mobile
	    ) AS U; 
	
	    IF user_count > 0 THEN 
	        RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';
	    END IF;
    
    ELSIF TG_OP = 'UPDATE' AND TG_TABLE_NAME = 'employees' THEN 
			SELECT COUNT(*) INTO user_count
	    FROM (
	        SELECT user_id 
	        FROM Customers C 
	        WHERE C.email = NEW.email OR C.mobile = NEW.mobile
	        UNION 
	        SELECT user_id 
	        FROM Employees E 
	        WHERE (E.email = NEW.email OR E.mobile = NEW.mobile) AND E.user_id != NEW.user_id
	        UNION 
	        SELECT user_id 
	        FROM Authors A 
	        WHERE A.email = NEW.email OR A.mobile = NEW.mobile
	    ) AS U; 
	
	    IF user_count > 0 THEN 
	        RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';
	    END IF;
    
    ELSIF TG_OP = 'UPDATE' AND TG_TABLE_NAME = 'authors' THEN 
      
			SELECT COUNT(*) INTO user_count
	    FROM (
	        SELECT user_id 
	        FROM Customers C 
	        WHERE C.email = NEW.email OR C.mobile = NEW.mobile
	        UNION 
	        SELECT user_id 
	        FROM Employees E 
	        WHERE E.email = NEW.email OR E.mobile = NEW.mobile
	        UNION 
	        SELECT user_id 
	        FROM Authors A 
	        WHERE (A.email = NEW.email OR A.mobile = NEW.mobile) AND A.user_id != NEW.user_id
	    ) AS U; 
	
	    IF user_count > 0 THEN 
	        RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';
	    END IF;
		END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

The above function checks for new user entry via `INSERT` or `UPDATE` is unique or not w.r.t. `user_id`, `mobile` and `email`

Define Trigger that executes this function to check uniqueness across all three tables.

```sql
CREATE TRIGGER customersNonOverlapTrigger
BEFORE INSERT OR UPDATE ON Customers
FOR EACH ROW 
EXECUTE FUNCTION checkUserUniqueness();
```

```sql
CREATE TRIGGER employeesNonOverlapTrigger
BEFORE INSERT OR UPDATE ON Employees
FOR EACH ROW 
EXECUTE FUNCTION checkUserUniqueness();
```

```sql
CREATE TRIGGER authorsNonOverlapTrigger
BEFORE INSERT OR UPDATE ON Authors
FOR EACH ROW 
EXECUTE FUNCTION checkUserUniqueness();
```

# Queries

## 1. Full Text Search Queries

**************************************************************Full Text Search on Author Bio************************************************************** 

Lets say customer user wants to know authors who’s interests are in statistical methods for data science.

```sql
SELECT A.given_name, A.last_name, A.bio
FROM authors as A
WHERE to_tsvector('english', A.bio) @@ plainto_tsquery('english', 'Statistical methods for data science');
```

**Full Text Search on Books description**

```sql
SELECT B.book_id, B.book_name, B.description 
FROM books as B
WHERE to_tsvector('english', B.description) @@ plainto_tsquery('english', 'No matter goals');
```

```sql
SELECT B.book_id, B.book_name, B.description 
FROM books as B
WHERE to_tsvector('english', B.description) @@ plainto_tsquery('english', 'Mockingbird novel');
```

****************************Full Text Search on Subscription description****************************

```sql
SELECT *
FROM subscriptions S
WHERE to_tsvector('english', S.description) @@ plainto_tsquery('english', 'Affordable access');
```

## 2. Query for Custom Types

**************************************************Queries for Custom Type************************************************** `ADDRESS_TYPE`

1. Let say we want to know customers from zip code 10027
    
    ```sql
    SELECT *
    FROM Customers C
    WHERE (C.address_details).zip_code = '10027';
    ```
    
2. Want to know Authors from Queens 
    
    ```sql
    SELECT *
    FROM authors A
    WHERE (A.address_details).city = 'Queens';
    ```
    

****************************************Queries for Custom Type**************************************** `PAYMENT_DETAILS`

1. Want to know Customers with payment mode set to `‘Debit card’` in zip code 10027
    
    ```sql
    SELECT *
    FROM customers C
    WHERE C.payment_details = 'Debit card' AND (C.address_details).zip_code = '10027';
    ```
    

## 3. Trigger Check Example (Total participation constraint of Books)

Simply executing the below transaction will violate the constraint and throw an exception.

```sql
BEGIN;
  INSERT INTO Books (
      book_name, 
      google_link
  ) VALUES (
      'COMS 4771 ML: Linear Regression Notes',
      'https://drive.google.com/file/d/1UFWfbUyBI-fmvDg0HR9F2Eg1CTNtBGJH/view?usp=sharing'
  );
COMMIT;
```

Single transaction in which the do block executes series of SQL queries successfully passing TRIGGER checks.

```sql
DO $$ 
DECLARE 
    new_book_id INTEGER;
BEGIN
    INSERT INTO Books (
        book_name, 
        google_link
    ) VALUES (
        'COMS 4771 ML: Linear Regression Notes',
        'https://drive.google.com/file/d/1UFWfbUyBI-fmvDg0HR9F2Eg1CTNtBGJH/view?usp=sharing'
    )
    RETURNING book_id INTO new_book_id;

    INSERT INTO classified_by (
        book_id, 
        section_id
    ) VALUES (
        new_book_id, 
        2
    );

    INSERT INTO written_by (
        book_id, 
        user_id
    ) VALUES (
        new_book_id, 
        'fd5f2ad39b544a4fac7e3bafb16e8419'
    );
END $$;
```

## 4. Trigger Check Example for unique user

This transaction will fail because it violates the non-overlapping constraint. Omkar already has a customer account with email `op2281@columbia.edu` so using the same email 

to create author account despite having different `user_id` and `mobile` will still throw an exception.

```sql
BEGIN;

INSERT INTO Authors (
    user_id,
    given_name,
    last_name,
    email,
    mobile,
    password
  )
VALUES (
    'ae47209334824faa97aa057443e0dsg0',
    'Omkar',
    'Pitale',
    'op2281@columbia.edu',
    '3479695594',
    'omkar@123'
  );

COMMIT;
```