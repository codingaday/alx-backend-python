import sqlite3
import functools
from datetime import datetime

#3rd week of Python Generators
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL
# )
# ''')

# cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
# cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
# conn.commit()
# conn.close()


# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument from the function call
        query = kwargs.get('query') or (args[0] if args else None)

        # Log the query to the console
        print(f"[SQL LOG] Executing query: {query}")

        # Call the actual function
        start_time = datetime.now()

        result = func(*args, **kwargs)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"[SQL LOG] Query executed in {duration:.4f} seconds")

        return result
    return wrapper

# Function that fetches users
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')            
    cursor = conn.cursor()                       
    cursor.execute(query)                         
    results = cursor.fetchall()                   
    conn.close()                                  
    return results                                 

# Run the function
users = fetch_all_users(query="SELECT * FROM users")
print(users)