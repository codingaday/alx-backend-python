from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    select_query = """SELECT * FROM user_data"""
    
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(select_query)
    
    batch = []
    for user in cursor:
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
    
    return True

