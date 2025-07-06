from mysql.connector import Error
import uuid
import mysql.connector
import csv

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'db_user'
DB_PASSWORD = '234fbc4ef8eedcd37f342'

def connect_db():
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to MySQL Server")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create the database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database="ALX_prodev"
        )
        print("Connected to ALX_prodev database")
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create table user_data if it does not exist with required fields"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,1) NOT NULL)
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table user_data created or already exists")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, data):
    """
    Insert data from CSV file into the database if it doesn't exist
    Args:
        connection: MySQL database connection
        data: Path to the CSV file containing user data
    """
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor = connection.cursor()
        inserted_count = 0

        with open(data, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    # Generate UUID for each user
                    user_id = str(uuid.uuid4())
                    record_data = (
                        user_id,
                        row['name'],
                        row['email'],
                        float(row['age'])
                    )
                    cursor.execute(insert_query, record_data)
                    inserted_count += 1
                except (ValueError, KeyError) as e:
                    print(f"Skipping malformed row: {row}. Error: {e}")
                    continue

        connection.commit()
        print(f"Successfully inserted {inserted_count} records into user_data table")

    except FileNotFoundError:
        print(f"Error: CSV file {csv_file_path} not found")

    except Error as e:
        print(f"Database error while inserting data: {e}")
        connection.rollback()

