from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor()
    
    cursor.execute("SELECT age FROM users WHERE age IS NOT NULL")
    for (age,) in cursor:
         yield age

    cursor.close()
    connection.close()

def calculate_average_age():
    total = 0
    count = 0
    
    for age in stream_user_ages():
        total += age
        count += 1
    
    if count == 0:
        return 0  # Avoid division by zero
    
    return total / count

# Calculate and print the average age
average_age = calculate_average_age()
print(f"Average age of users: {average_age:.2f}")

