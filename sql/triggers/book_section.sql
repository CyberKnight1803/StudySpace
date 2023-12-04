CREATE OR REPLACE FUNCTION checkBookSectionParticipationInClassified_by() RETURNS TRIGGER AS $$ BEGIN IF TG_OP = 'DELETE' THEN IF (
    SELECT COUNT(*)
    FROM Classified_by C
    WHERE C.book_id = OLD.book_id
  ) = 0
  AND (
    SELECT COUNT(*)
    FROM Books B
    WHERE B.book_id = OLD.book_id
  ) = 1 THEN
INSERT INTO Classified_by(
    book_id,
    section_id
  )
VALUES (
    OLD.book_id,
    OLD.section_id
  );

RAISE EXCEPTION 'Total Participation Constraint Violation';

END IF;

ELSIF TG_OP = 'UPDATE' THEN IF (
  SELECT COUNT(*)
  FROM Classified_by C
  WHERE C.book_id = OLD.book_id
) = 0 THEN RAISE EXCEPTION 'Total Participation Constraint Violation';

END IF;

END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION checkBookSectionParticipationInBooks() RETURNS TRIGGER AS $$ BEGIN IF TG_OP = 'INSERT' THEN IF (
    SELECT COUNT(*)
    FROM Classified_by C
    WHERE C.book_id = NEW.book_id
  ) = 0 THEN
DELETE FROM Books B
WHERE B.book_id = NEW.book_id;

RAISE EXCEPTION 'Total Participation Constraint Violation';

END IF;

ELSIF TG_OP = 'UPDATE' THEN IF (
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

CREATE CONSTRAINT TRIGGER BookSectionTotalParticipationTrigger
AFTER
INSERT
  OR
UPDATE ON Books DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION checkBookSectionParticipationInBooks();

CREATE CONSTRAINT TRIGGER BookSectionTotalParticipationTrigger
AFTER
UPDATE
  OR DELETE ON Classified_by DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION checkBookSectionParticipationInClassified_by();