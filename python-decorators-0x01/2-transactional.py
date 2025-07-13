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


# Transaction decorator
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Call the actual DB operation
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print("Transaction rolled back due to error:", str(e))
            raise e
    return wrapper

# Decorated DB update function
@with_db_connection     
@transactional          
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    print(f"User {user_id} email updated to {new_email}.")

# Call the function to update user email
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
