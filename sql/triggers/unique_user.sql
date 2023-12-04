CREATE OR REPLACE FUNCTION checkUserUniqueness() RETURNS TRIGGER AS $$
DECLARE user_count INT;

BEGIN IF TG_OP = 'INSERT' THEN
SELECT COUNT(*) INTO user_count
FROM (
    SELECT user_id
    FROM Customers C
    WHERE C.user_id = NEW.user_id
      OR C.email = NEW.email
      OR C.mobile = NEW.mobile
    UNION
    SELECT user_id
    FROM Employees E
    WHERE E.user_id = NEW.user_id
      OR E.email = NEW.email
      OR E.mobile = NEW.mobile
    UNION
    SELECT user_id
    FROM Authors A
    WHERE A.user_id = NEW.user_id
      OR A.email = NEW.email
      OR A.mobile = NEW.mobile
  ) AS U;

IF user_count > 0 THEN RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';

END IF;

ELSIF TG_OP = 'UPDATE'
AND TG_TABLE_NAME = 'customers' THEN
SELECT COUNT(*) INTO user_count
FROM (
    SELECT user_id
    FROM Customers C
    WHERE (
        C.email = NEW.email
        OR C.mobile = NEW.mobile
        AND C.user_id != NEW.user_id
        UNION
        SELECT user_id
        FROM Employees E
        WHERE E.email = NEW.email
          OR E.mobile = NEW.mobile
        UNION
        SELECT user_id
        FROM Authors A
        WHERE A.email = NEW.email
          OR A.mobile = NEW.mobile
      ) AS U;

IF user_count > 0 THEN RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';

END IF;

ELSIF TG_OP = 'UPDATE'
AND TG_TABLE_NAME = 'employees' THEN
SELECT COUNT(*) INTO user_count
FROM (
    SELECT user_id
    FROM Customers C
    WHERE C.email = NEW.email
      OR C.mobile = NEW.mobile
    UNION
    SELECT user_id
    FROM Employees E
    WHERE (
        E.email = NEW.email
        OR E.mobile = NEW.mobile
      )
      AND E.user_id != NEW.user_id
    UNION
    SELECT user_id
    FROM Authors A
    WHERE A.email = NEW.email
      OR A.mobile = NEW.mobile
  ) AS U;

IF user_count > 0 THEN RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';

END IF;

ELSIF TG_OP = 'UPDATE'
AND TG_TABLE_NAME = 'authors' THEN
SELECT COUNT(*) INTO user_count
FROM (
    SELECT user_id
    FROM Customers C
    WHERE C.email = NEW.email
      OR C.mobile = NEW.mobile
    UNION
    SELECT user_id
    FROM Employees E
    WHERE E.email = NEW.email
      OR E.mobile = NEW.mobile
    UNION
    SELECT user_id
    FROM Authors A
    WHERE (
        A.email = NEW.email
        OR A.mobile = NEW.mobile
      )
      AND A.user_id != NEW.user_id
  ) AS U;

IF user_count > 0 THEN RAISE EXCEPTION 'Non-Overlap Constraint Violation: Users with same user_id, email or mobile already exists.';

END IF;

END IF;

RETURN NEW;

END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER customersNonOverlapTrigger BEFORE
INSERT
  OR
UPDATE ON Customers FOR EACH ROW EXECUTE FUNCTION checkUserUniqueness();

CREATE OR REPLACE TRIGGER employeesNonOverlapTrigger BEFORE
INSERT
  OR
UPDATE ON Employees FOR EACH ROW EXECUTE FUNCTION checkUserUniqueness();

CREATE OR REPLACE TRIGGER authorsNonOverlapTrigger BEFORE
INSERT
  OR
UPDATE ON Authors FOR EACH ROW EXECUTE FUNCTION checkUserUniqueness();