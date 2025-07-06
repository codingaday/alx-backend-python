# 🧬 Seed Script – User Data Seeding to MySQL

## 📁 Directory: `python-generators-0x00`

This script is part of the **ALX Backend Python Track** and handles:

- Database connection
- Creating a MySQL database and table
- Populating data from a CSV file

---

## 📦 Files

- `seed.py`: Python script to create database, table, and insert user data.
- `user_data.csv`: CSV file with user records.

---

## 🧪 Features

- Creates database `ALX_prodev` if not existing.
- Creates table `user_data` with fields:
  - `user_id` (UUID, PK, Indexed)
  - `name` (VARCHAR)
  - `email` (VARCHAR)
  - `age` (DECIMAL)
- Prevents duplicate entries based on email.
- Loads data from `user_data.csv`.

---

## 🛠️ Function Prototypes

```python
def connect_db() -> mysql.connector.connection:
    # Connects to MySQL server

def create_database(connection):
    # Creates ALX_prodev database

def connect_to_prodev() -> mysql.connector.connection:
    # Connects to ALX_prodev DB

def create_table(connection):
    # Creates user_data table

def insert_data(connection, filename):
    # Inserts data from CSV into DB
```

---

## 🚀 Main file to test seed.py

```python
seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
```

## 🧩 Requirements

- Python 3.x
- `mysql-connector-python`

## 📌 Notes

- Ensure MySQL server is running and credentials in `seed.py` are valid
- Place `user_data.csv` in the same directory as `seed.py`
- run `0-main.py`

---

## 📦 Additional Files

- `0-stream_users.py`: Streams users one by one

  - Place `0-stream_users.py` in the same directory as `seed.py`
  - Use `1-main.py` to test this file

- `1-batch_processing.py`: Processes users in batches

  - Place `1-batch_processing.py` in the same directory as `seed.py`
  - Use `2-main.py` to test this file

- `2-lazy_paginate.py`: Paginates users with lazy loading

  - Place `2-lazy_paginate.py` in the same directory as `seed.py`
  - Use `3-main.py` to test this file

- `4-stream_ages.py`: Streams user ages and computes average
  - Place `4-stream_ages.py` in the same directory as `seed.py`
