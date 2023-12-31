# StudySpace

### PostgreSQL account

Account: `op2281`

### Website

URL: `http://35.196.70.132:8111`

## Features Implemented

### Customers

- Authentication  
  a. Customers can Login, Logout.  
  b. Users can signup and create their customer account.

- Profile  
  a. Customers can update their profile details  
  b. Customers can reset their password  
  c. Customers can purchase a subscription plan according to their needs.

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
- Books  
  a. Authors can add books, along with who gets to access them.  
  b. Authors can view all the books they have written and posted.
- Profile  
  a. Authors can see all their information.  
  b. Authors can update their profile information.

### Employees

- Authentication  
  a. Employees can Login, Logout.  
  b. An employee can not be registered via the portal, can be done only by superadmin on backend.
- Profile  
  a. Employees can see all their information.
  b. Employees can update their profile information.
- Views  
  a. Employees can view all books.  
  b. Employees can view all customers.  
  c. Employees can view all authors.  
  d. Employees can view all payment transactions.  
  e. Employees can view all publishers.

- Changes  
  a. Employees can add publishers (Only employees can do this).  
  b. Employees can verify authors.
- Deletions  
  a. Employees can remove customers.  
  b. Employees can remove books.

## Features Not Implemented

Contraints requiring triggers. Eg: Total Participation Constraint

## Interesting WebPage - 1

### Search System

Customers can use the search filtering option we provide to search books faster in our studyspace.

To access this website the customer must login first, so that the search system will be present on webpage -  
`http://35.196.70.132:8111/customer`

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

### Employee Page

The Employee has complete control over all the elements of the website and its underlying database.

There are some access rights only employees get:

1. Verifying authors
2. Adding Publishers

In addition to this, employees also have the power to force remove entries from our system. Employees can -

1. Remove customers
2. Remove books

Employees can also view all the information present in the database -

1. View all authors. (Only employees have access)
2. View all books.  
   Note that this is not just what is in the books database, but a compilation across multiple databases including all authors of a book etc. All the book information across multiple entities is also captured in the view more section of every book after search (previous webpage).
3. View all payments. (Only employees have access)  
   Again, similar to books, employees can access all the information across multiple database entities for every payment, i.e. subscription type, price, time, user id etc.
4. View all publishers. (Only employees have access)

To access this page, the employee needs to login from this url -  
`http://35.196.70.132:8111/employee/login`

The url of the page described above is -  
`http://35.196.70.132:8111/employee`

## Example Login Details

Customer Logins : `op2281@columbia.edu`  
Customer Passwords : `omkar@123`

Author Logins : `jamesclear@gmail.com`  
Author Passwords : `habitmaster123`

Employee Logins : `john.doe@studyspace.com`  
Employee Passwords : `john@doe`

You can find more logins and passwords inside the Authors.csv, Customers.csv and Employees.csv files in the /data folder.
