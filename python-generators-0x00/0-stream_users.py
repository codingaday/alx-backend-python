import sqlite3
import functools


#2nd week of Python Generators
from seed import connect_to_prodev

def stream_users():
    connection = connect_to_prodev()

    select_query = """SELECT * FROM user_data"""

    cursor = connection.cursor(dictionary=True)
    cursor.execute(select_query)

    for user in cursor:
        yield user

    cursor.close()
    connection.close()



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


import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument from the function call
        query = kwargs.get('query') or (args[0] if args else None)

        # Log the query to the console
        print(f"[SQL LOG] Executing query: {query}")

        # Call the actual function
        result = func(*args, **kwargs)

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


