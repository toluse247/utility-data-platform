CREATE KEYSPACE utility_db WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'}  AND durable_writes = true;  

CREATE TABLE utility_db.payments (
    payment_id int PRIMARY KEY,
    customer_id int,
    payment_amount float,
    payment_channel text,
    payment_timestamp timestamp
);