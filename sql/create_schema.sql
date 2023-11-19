CREATE TABLE Customers (
    user_id CHAR(32),
    given_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    mobile CHAR(10) CHECK (mobile ~ '^[1-9][0-9]{9}$'),
    email VARCHAR(50) NOT NULL CHECK (
        email ~ '^[a-z]([a-z0-9]*\.)*[a-z0-9]+@([a-z]+\.)+[a-z]+$'
    ),
    password VARCHAR(30) NOT NULL CHECK (password ~ '^[a-zA-Z0-9@$.]{5,}$'),
    address VARCHAR(60),
    payment_details VARCHAR(20) CHECK (
        payment_details = 'Apple pay'
        OR payment_details = 'Google pay'
        OR payment_details = 'Credit card'
        OR payment_details = 'Debit card'
    ),
    subscription_status BOOLEAN DEFAULT FALSE,
    CHECK (
        NOT (
            subscription_status
            AND payment_details is NULL
        )
    ),
    UNIQUE (email),
    UNIQUE (mobile),
    PRIMARY KEY (user_id)
);

CREATE TABLE Employees (
    user_id CHAR(32),
    given_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    mobile CHAR(10) CHECK (mobile ~ '^[1-9][0-9]{9}$'),
    email VARCHAR(50) NOT NULL CHECK (
        email ~ '^[a-z]([a-z0-9]*\.)*[a-z0-9]+@studyspace.com$'
    ),
    password VARCHAR(30) NOT NULL CHECK (password ~ '^[a-zA-Z0-9@$.]{5,}$'),
    address VARCHAR(60) NOT NULL,
    ssn CHAR(11) NOT NULL CHECK (
        ssn ~ '^[0-9]{3}-[0-9]{2}-[0-9]{4}$'
    ),
    UNIQUE (email),
    UNIQUE (mobile),
    UNIQUE (ssn),
    PRIMARY KEY (user_id)
);

CREATE TABLE Authors (
    user_id CHAR(32),
    given_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    mobile CHAR(10) CHECK (mobile ~ '^[1-9][0-9]{9}$'),
    email VARCHAR(50) NOT NULL CHECK (
        email ~ '^[a-z]([a-z0-9]*\.)*[a-z0-9]+@([a-z]+\.)+[a-z]+$'
    ),
    password VARCHAR(30) NOT NULL CHECK (password ~ '^[a-zA-Z0-9@$.]{5,}$'),
    is_verified BOOLEAN DEFAULT FALSE,
    UNIQUE (email),
    UNIQUE (mobile),
    PRIMARY KEY (user_id)
);

CREATE TABLE Books (
    book_id SERIAL,
    book_name VARCHAR(80) NOT NULL,
    edition INT CHECK (edition > 0),
    pages INT CHECK (pages > 0),
    publication_year INT,
    description VARCHAR(1000),
    language VARCHAR(100),
    google_link VARCHAR(150) NOT NULL,
    PRIMARY KEY (book_id)
);

CREATE TABLE PaymentTransactions (
    transaction_id SERIAL,
    time_stamp TIMESTAMP,
    PRIMARY KEY (transaction_id)
);

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
    FOREIGN KEY (book_id) REFERENCES Books ON DELETE CASCADE,
    FOREIGN KEY (publisher_id) REFERENCES Publishers
);

CREATE TABLE Classified_by (
    book_id INT,
    section_id INT,
    PRIMARY KEY (book_id, section_id),
    FOREIGN KEY (book_id) REFERENCES Books ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES Sections
);

CREATE TABLE Written_by (
    user_id CHAR(32),
    book_id INT,
    PRIMARY KEY (user_id, book_id),
    FOREIGN KEY (user_id) REFERENCES Authors,
    FOREIGN KEY (book_id) REFERENCES Books ON DELETE CASCADE
);

CREATE TABLE Subscribe (
    user_id CHAR(32),
    subscription_id INT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    CHECK (end_date = start_date + '1 year'),
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES Customers ON DELETE CASCADE,
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions
);

CREATE TABLE Accessed_by (
    book_id INT,
    subscription_id INT,
    PRIMARY KEY (book_id, subscription_id),
    FOREIGN KEY (book_id) REFERENCES Books ON DELETE CASCADE,
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions
);

CREATE TABLE Payments (
    user_id CHAR(32),
    transaction_id INT,
    subscription_id INT NOT NULL,
    PRIMARY KEY (user_id, transaction_id),
    FOREIGN KEY (user_id) REFERENCES Customers ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES PaymentTransactions,
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions
);