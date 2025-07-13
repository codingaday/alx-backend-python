import time
import sqlite3
import functools
from datetime import datetime

#3rd week of Python Generators

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open the connection
        conn = sqlite3.connect('users.db')
        print("Opening database connection...")
        try:
            # Pass the open connection to the function
            print("Connection opened.")
            start_time = datetime.now()

            result =  func(conn, *args, **kwargs)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"Function executed in {duration:.4f} seconds")
            return result
        finally:
            # Always close the connection
            conn.close()
            print("Connection closed.")
    
    return wrapper

# Retry-on-failure decorator factory
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs) 
                except Exception as e:
                    attempt += 1
                    print(f"[Attempt {attempt}] Error: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print("Max retries reached. Operation failed.")
                        raise e 
        return wrapper
    return decorator

# Function to fetch users with retry logic
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Try it!
users = fetch_users_with_retry()
print(users)
