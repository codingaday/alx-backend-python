import sqlite3

# class-based context manager that runs any query with parameters
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name        
        self.query = query            
        self.params = params or ()    
        self.conn = None              
        self.result = None            

    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        # Execute the query with parameters
        cursor.execute(self.query, self.params)
        # Fetch results and store in instance
        self.result = cursor.fetchall()
        return self.result           

    def __exit__(self, type, val, tb):
        # Always close connection
        if self.conn:
            self.conn.close()
            print("Connection closed.")

# get users over age 25
query = "SELECT * FROM users WHERE age > ?"
params = (25,)  

with ExecuteQuery("users.db", query, params) as results:
    print("Users over 25:")
    for row in results:
        print(row)


