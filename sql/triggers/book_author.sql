CREATE OR REPLACE FUNCTION checkBookAuthorParticipationInWritten_by() RETURNS TRIGGER AS $$ BEGIN IF TG_OP = 'DELETE' THEN IF (
    SELECT COUNT(*)
    FROM Written_by W
    WHERE W.book_id = OLD.book_id
  ) = 0
  AND (
    SELECT COUNT(*)
    FROM Books B
    WHERE B.book_id = OLD.book_id
  ) = 1 THEN
INSERT INTO Written_by(
    book_id,
    author_id
  )
VALUES (
    OLD.book_id,
    OLD.author_id
  );

RAISE EXCEPTION 'Total Participation Constraint Violation';

END IF;

ELSIF TG_OP = 'UPDATE' THEN IF (
  SELECT COUNT(*)
  FROM Written_by W
  WHERE W.book_id = OLD.book_id
) = 0 THEN RAISE EXCEPTION 'Total Participation Constraint Violation';

END IF;

END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION checkBookAuthorParticipationInBooks() RETURNS TRIGGER AS $$ BEGIN IF TG_OP = 'INSERT' THEN IF (
    SELECT COUNT(*)
    FROM Written_by W
    WHERE W.book_id = NEW.book_id
  ) = 0 THEN
DELETE FROM Books B
WHERE B.book_id = NEW.book_id;

RAISE EXCEPTION 'Total Participation Constraint Violation';

END IF;

ELSIF TG_OP = 'UPDATE' THEN IF (
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
AFTER
INSERT
  OR
UPDATE ON Books DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION checkBookAuthorParticipationInBooks();

CREATE CONSTRAINT TRIGGER BookAuthorTotalParticipationTrigger
AFTER
UPDATE
  OR DELETE ON Written_by DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION checkBookAuthorParticipationInWritten_by();