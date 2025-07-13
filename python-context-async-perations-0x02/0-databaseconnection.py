import sqlite3
# Define custom context manager
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name      
        self.conn = None            
    
    def __enter__(self):
        # Open connection when 'with' block starts
        self.conn = sqlite3.connect(self.db_name)
        print("Database connection opened.")
        return self.conn            

    def __exit__(self, type, val, tb):
        # Always called at the end of 'with' block
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Use the context manager to run a query
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)

