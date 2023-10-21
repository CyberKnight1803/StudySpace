-- Query 1
SELECT A.user_id,
  A.given_name,
  A.last_name,
  COUNT(DISTINCT C.section_id) AS number_of_sections
FROM authors A,
  written_by W,
  classified_by C
WHERE A.user_id = W.user_id
  AND W.book_id = C.book_id
GROUP BY A.user_id
ORDER BY number_of_sections DESC;

-- Query 2
-- Query 3
-- Query 4