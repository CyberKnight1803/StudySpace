# StudySpace

### PostgreSQL account

Account: `op2281`

### Website

URL: `http://<IP>:8111`

## Features Implemented

### Customers

- Authentication  
  a. Customers can Login, Logout.  
  b. Users can signup and create their customer account.

- Profile  
  a. ustomers can update their profile details  
  b. Customers can reset their password  
  c. Cusomters can purchase a subscription plan according to their needs.

- Transaction History  
  Customer can see their payment history

- Search  
  Sophisticated search system to search books  
   a. Supports title search [substring matching in SQL]  
   b. Filter by edition  
   c. Supports author search [substring matching in SQL]  
   d. Filter by publication years  
   e. Filter by section

### Authors

- Authentication  
  a. Authors can Login, Logout.  
  b. Users can signup and create their author account if they wish to publish books.

### Employees

- Authentication  
  a. Employees can Login, Logout.  
  b. An employee can not be registered via the portal, can be done only by superadmin on backend.

## Features Not Implemented

Contraints requiring triggers. Eg: Total Participation Constraint

## Interesting WebPage - 1

### Search System

Customers can use the search filtering option we provide to search books faster in our studyspace.

To access this website the customer must login first, so that the search system will be present on webpage -  
`http://<IP>:8111/customer`

Sophisticated search system to search books  
 a. Supports title search [substring matching in SQL]  
 b. Filter by edition  
 c. Supports author search [substring matching in SQL]  
 d. Filter by publication years  
 e. Filter by section

### Magical SQL Query for search filtering

```
SELECT B.book_id,
    B.book_name,
    B.edition,
    B.publication_year,
    STRING_AGG(DISTINCT CONCAT(A.given_name, ' ', A.last_name), ', ') AS author_names,
    STRING_AGG(DISTINCT section_name, ', ') AS sections
  FROM Books B
    JOIN Written_by WB ON B.book_id = WB.book_id
    JOIN Authors A ON WB.user_id = A.user_id
    JOIN Classified_by CB ON B.book_id = CB.book_id
    JOIN Sections S ON CB.section_id = S.section_id
  WHERE LOWER(B.book_name) LIKE '%' || LOWER(:title) || '%' <- DYNAMIC
    AND B.publication_year BETWEEN :from_year AND :to_year <- DYNAMIC
    AND CONCAT(LOWER(A.given_name), ' ', LOWER(A.last_name)) LIKE '%' || LOWER(:author_name) || '%' <- DYNAMIC
    AND B.edition = :edition        <- DYNAMIC
    AND S.section_id=:section_id    <- DYNAMIC
  GROUP BY
    B.book_id,
    B.book_name,
    B.edition,
    B.publication_year;
```

### What makes this query interesting?

The substring match should be case insensitive , so we use the `LOWER` function provided by `POSTGRESQL` for substring search.

Since we have so many options for filter search, we need to add the search conditions dynamically into our `WHERE` clause.

The real challenge here was since one book can be written by multiple authors and can be classified in multiple sections so we end up with multiple tuples because `author name` and `section name` can be different. To tackle this we use the `GROUP BY` clause and use `STRING_AGG` aggregation to get the `author names` and `section names` in a comma separated fashion in a string.

### Interpreting Search Results

Once we have given some filters as input, we project the search results with view more details link, so user can see more details about the book.  
**NOTE**: The search results show all books regardless of the subscription policy the user is subscribed to.

To access the book, you need to click on view more which leads to the page -  
`http://<IP>:8111/books/book?book_id=<book_id>`

Which will show more details about the book also, based on your subscription plan, you can get the link to access the book as a pdf.

## Interesting WebPage - 2
