
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





