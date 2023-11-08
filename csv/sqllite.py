import uuid
import sqlite3

def generate_uuid():
    return str(uuid.uuid4())

def find_uuid_by_reference(connection, reference):
    query = "SELECT UUID FROM UUID_TABLE WHERE REFERENCE = ?"
    cursor = connection.cursor()
    cursor.execute(query, (reference,))
    result = cursor.fetchone()
    return result[0] if result else None

def update_or_insert_uuid_to_sqlite(connection, reference, uuid_value):
    try:
        existing_uuid = find_uuid_by_reference(connection, reference)

        cursor = connection.cursor()
        # If the reference exists, update the UUID
        if existing_uuid:
            update_query = "UPDATE UUID_TABLE SET UUID = ? WHERE REFERENCE = ?"
            cursor.execute(update_query, (uuid_value, reference))
        else:
            # If the reference doesn't exist, insert a new row
            insert_query = "INSERT INTO UUID_TABLE (REFERENCE, UUID) VALUES (?, ?)"
            cursor.execute(insert_query, (reference, uuid_value))

        connection.commit()
        print("UUID updated/inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
sqlite_file = 'uuid_records.sqlite'
connection = sqlite3.connect(sqlite_file)

# Create the table if it doesn't exist
with connection:
    connection.execute('''
        CREATE TABLE IF NOT EXISTS UUID_TABLE (
            REFERENCE TEXT PRIMARY KEY,
            UUID TEXT
        )
    ''')

references = ['user_1', 'product_42', 'order_123']
for reference in references:
    generated_uuid = generate_uuid()
    update_or_insert_uuid_to_sqlite(connection, reference, generated_uuid)

# Don't forget to close the connection when you're done
connection.close()

