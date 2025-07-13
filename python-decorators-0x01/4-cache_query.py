import time
import sqlite3
import functools

#3rd week of Python Generators

# In-memory cache to store query results
query_cache = {}

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
            start_time = time.time()
         
            result =  func(conn, *args, **kwargs)
            
            end_time = time.time()
            duration = (end_time - start_time)
            print(f"Function executed in {duration:.4f} seconds")
            return result
        finally:
            # Always close the connection
            conn.close()
            print("Connection closed.")
    
    return wrapper

# ✅ Caching decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query string
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)

        # Check if result is already cached
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]
        
        # If not cached, run the DB function
        result = func(*args, **kwargs)

        # Cache the result using query string as key
        query_cache[query] = result
        print(f"[CACHE MISS] Caching result for: {query}")

        return result
    return wrapper

# ✅ Function to fetch users, now with caching
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ First call — triggers DB access
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# ✅ Second call — uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
