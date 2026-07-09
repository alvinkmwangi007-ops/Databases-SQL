import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "data.sqlite"


def initialize_database() -> None:
    """Create a small SQLite database with the tables used in the lab."""
    if DB_PATH.exists():
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE employees (
            employeeNumber INTEGER PRIMARY KEY,
            lastName TEXT NOT NULL,
            firstName TEXT NOT NULL,
            jobTitle TEXT NOT NULL
        );

        CREATE TABLE orders (
            orderNumber INTEGER PRIMARY KEY,
            orderDate TEXT NOT NULL
        );

        CREATE TABLE orderDetails (
            orderNumber INTEGER NOT NULL,
            priceEach REAL NOT NULL,
            quantityOrdered INTEGER NOT NULL,
            FOREIGN KEY(orderNumber) REFERENCES orders(orderNumber)
        );

        INSERT INTO employees (employeeNumber, lastName, firstName, jobTitle) VALUES
            (1002, 'Murphy', 'Diane', 'President'),
            (1056, 'Patterson', 'Mary', 'VP Sales'),
            (1076, 'Firrelli', 'Jeff', 'VP Marketing'),
            (1088, 'Patterson', 'William', 'Sales Manager (APAC)'),
            (1102, 'Bondur', 'Gerard', 'Sale Manager (EMEA)');

        INSERT INTO orders (orderNumber, orderDate) VALUES
            (10100, '2003-01-06'),
            (10101, '2003-01-09'),
            (10102, '2003-01-10');

        INSERT INTO orderDetails (orderNumber, priceEach, quantityOrdered) VALUES
            (10100, 101.00, 2),
            (10101, 56.25, 4),
            (10102, 89.99, 3);
        """
    )

    conn.commit()
    conn.close()


initialize_database()
conn = sqlite3.connect(DB_PATH)

# STEP 1A
# Import SQL Library and Pandas

# STEP 1B
# Connect to the database
# conn is already established above

# STEP 2
# Replace None with your code
# Query employee number and last name for all employees
# The result should only contain those two columns.
df_first_five = pd.read_sql("""
SELECT employeeNumber, lastName
FROM employees
""", conn)

# STEP 3
# Repeat Step 2, but have the last name come before the employee number
df_five_reverse = pd.read_sql("""
SELECT lastName, employeeNumber
FROM employees
""", conn)

# STEP 4
# Use an alias to rename the employee number column as 'ID'
df_alias = pd.read_sql("""
SELECT employeeNumber AS ID, lastName
FROM employees
""", conn)

# STEP 5
# Use CASE to classify executives based on job title
df_executive = pd.read_sql("""
SELECT employeeNumber, lastName, jobTitle,
       CASE
           WHEN jobTitle IN ('President', 'VP Sales', 'VP Marketing') THEN 'Executive'
           ELSE 'Not Executive'
       END AS role
FROM employees
""", conn)

# STEP 6
# Find the length of the last name and return as a new column
df_name_length = pd.read_sql("""
SELECT LENGTH(lastName) AS name_length
FROM employees
""", conn)

# STEP 7
# Return the first two letters of each job title
df_short_title = pd.read_sql("""
SELECT SUBSTR(jobTitle, 1, 2) AS short_title
FROM employees
""", conn)

# STEP 8
# Find the total amount for all orders using rounded total prices
order_details = pd.read_sql("""
SELECT *
FROM orderDetails
""", conn)

sum_total_price = pd.read_sql("""
SELECT ROUND(priceEach * quantityOrdered, 2) AS total_price
FROM orderDetails
""", conn)["total_price"].sum()

# STEP 9
# Return the original order date plus day, month, and year columns
df_day_month_year = pd.read_sql("""
SELECT orderDate,
       strftime('%d', orderDate) AS day,
       strftime('%m', orderDate) AS month,
       strftime('%Y', orderDate) AS year
FROM orders
""", conn)


if __name__ == "__main__":
    employee_data = pd.read_sql("""SELECT * FROM employees""", conn)
    print("---------------------Employee Data---------------------")
    print(employee_data)
    print("-------------------End Employee Data-------------------")

    print("------------------Order Details Data------------------")
    print(order_details)
    print("----------------End Order Details Data----------------")

    conn.close()
