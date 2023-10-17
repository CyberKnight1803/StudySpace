CREATE TABLE Customers (
    customer_id CHAR(32),
    given_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    mobile CHAR(10),
    email VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    address VARCHAR(60),
    payment_details VARCHAR(20) CHECK(
        payment_details = 'Apple pay'
        or payment_details = 'Google pay'
        or payment_details = 'Credit card'
        or payment_details = 'Debit card'
    ),
    subscription_status BOOLEAN DEFAULT FALSE,
    UNIQUE (email),
    UNIQUE (mobile),
    PRIMARY KEY (customer_id)
);

CREATE TABLE Employees (
    employee_id CHAR(32),
    given_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    mobile CHAR(10),
    email VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    address VARCHAR(60),
    ssn CHAR(13) NOT NULL,
    UNIQUE (email),
    UNIQUE (mobile),
    UNIQUE (ssn),
    PRIMARY KEY (employee_id)
);

CREATE TABLE Authors (
    author_id CHAR(32),
    given_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    mobile CHAR(10),
    email VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    UNIQUE (email),
    UNIQUE (mobile),
    PRIMARY KEY (author_id)
);

CREATE TABLE Books (
    book_id SERIAL,
    book_name VARCHAR(80) NOT NULL,
    edition INT,
    pages INT,
    publication_year INT,
    description VARCHAR(200),
    language VARCHAR(100),
    google_link VARCHAR(60) NOT NULL,
    PRIMARY KEY (book_id)
);

CREATE TABLE PaymentTransactions (
    transaction_id SERIAL,
    time_stamp TIMESTAMP,
    PRIMARY KEY (transaction_id)
);

-- Yet to add subscription_cost > 0 constraint
CREATE TABLE Subscriptions (
    subscription_id SERIAL,
    subscription_name VARCHAR(30) NOT NULL,
    subscription_cost REAL NOT NULL CHECK(subscription_cost > 0),
    description VARCHAR(100),
    UNIQUE (subscription_name),
    PRIMARY KEY (subscription_id)
);

CREATE TABLE Sections (
    section_id SERIAL,
    section_name VARCHAR(40) NOT NULL,
    UNIQUE (section_name),
    PRIMARY KEY (section_id)
);

CREATE TABLE Publishers (
    publisher_id SERIAL,
    publisher_name VARCHAR(50) NOT NULL,
    UNIQUE (publisher_name),
    PRIMARY KEY (publisher_id)
);

CREATE TABLE Published_by (
    book_id INT,
    publisher_id INT NOT NULL,
    PRIMARY KEY (book_id),
    FOREIGN KEY (book_id) REFERENCES Books,
    FOREIGN KEY (publisher_id) REFERENCES Publishers
);

CREATE TABLE Classified_by (
    book_id INT,
    section_id INT,
    PRIMARY KEY (book_id, section_id),
    FOREIGN KEY (book_id) REFERENCES Books,
    FOREIGN KEY (section_id) REFERENCES Sections
);

CREATE TABLE Written_by (
    author_id CHAR(32),
    book_id INT,
    PRIMARY KEY (author_id, book_id),
    FOREIGN KEY (author_id) REFERENCES Authors,
    FOREIGN KEY (book_id) REFERENCES Books
);

CREATE TABLE Subscribe (
    customer_id CHAR(32),
    subscription_id INT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    PRIMARY KEY (customer_id),
    FOREIGN KEY (customer_id) REFERENCES Customers,
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions
);

CREATE TABLE Accessed_by (
    book_id INT,
    subscription_id INT,
    PRIMARY KEY (book_id, subscription_id),
    FOREIGN KEY (book_id) REFERENCES Books,
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions
);

CREATE TABLE Payments (
    customer_id CHAR(32),
    transaction_id INT,
    subscription_id INT NOT NULL,
    PRIMARY KEY (customer_id, transaction_id),
    FOREIGN KEY (customer_id) REFERENCES Customers,
    FOREIGN KEY (transaction_id) REFERENCES PaymentTransactions,
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions
);