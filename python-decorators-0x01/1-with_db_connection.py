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

# Function to fetch a user by ID
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()                                      
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))  
    return cursor.fetchone()                                   

# Call the function — connection is auto-managed!
user = get_user_by_id(user_id=1)
print(user)
