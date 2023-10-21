SELECT B.book_id,
  B.book_name,
  B.publication_year
FROM Books B,
  Accessed_by A
WHERE B.publication_year > 2000
  AND A.book_id = B.book_id
GROUP BY B.book_id
HAVING COUNT(A.subscription_id) = 2;