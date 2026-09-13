CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    age INT,
    gender VARCHAR(20),
    city VARCHAR(50),
    signup_date DATE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    price NUMERIC(10,2)
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    product_id INT REFERENCES products(product_id),
    session_id VARCHAR(50),
    event_type VARCHAR(20),
    event_timestamp TIMESTAMP,
    experiment_group VARCHAR(20)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    product_id INT REFERENCES products(product_id),
    order_date TIMESTAMP,
    quantity INT,
    amount NUMERIC(10,2)
);
