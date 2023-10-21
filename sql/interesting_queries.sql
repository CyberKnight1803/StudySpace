-- Query 1 How many distinct sections every customer has access to
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

-- Query 2 Selecting all customers who bought the more expensive subscription and renewed it at least once
SELECT A.user_id,
  A.given_name,
  A.last_name,
  A.email,
  COUNT(P.transaction_id) AS number_of_renewals
FROM Customers A,
  Payments P
WHERE A.user_id = P.user_id
  AND P.subscription_id = 2
GROUP BY A.user_id
HAVING COUNT(P.transaction_id) >= 2
ORDER BY number_of_renewals DESC;

-- Query 3 books accessible by both subscriptions and published after 2000
SELECT B.book_id,
  B.book_name,
  B.publication_year
FROM Books B,
  Accessed_by A
WHERE B.publication_year > 2000
  AND A.book_id = B.book_id
GROUP BY B.book_id
HAVING COUNT(A.subscription_id) = 2;

-- Query 4 All users that transacted payments in both August and September 2023
SELECT C.user_id,
  C.given_name,
  C.last_name
FROM Customers C,
  PaymentTransactions T,
  Payments P
WHERE T.transaction_id = P.transaction_id
  AND TO_CHAR(T.time_stamp, 'YYYY-MM-DD-HH24.MI.SS.FF6') ~ '^.*-0[89]-.*$'
  AND P.user_id = C.user_id
GROUP BY C.user_id
HAVING COUNT(T.time_stamp) = 2;