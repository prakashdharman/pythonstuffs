import uuid
import cx_Oracle

def generate_uuid():
    return str(uuid.uuid4())

def find_uuid_by_reference(connection, reference):
    query = "SELECT UUID FROM UUID_TABLE WHERE REFERENCE = :1"
    with connection.cursor() as cursor:
        cursor.execute(query, (reference,))
        result = cursor.fetchone()
        return result[0] if result else None

def update_or_insert_uuid_to_oracle(connection, reference, uuid_value):
    try:
        existing_uuid = find_uuid_by_reference(connection, reference)

        with connection.cursor() as cursor:
            # If the reference exists, update the UUID
            if existing_uuid:
                update_query = "UPDATE UUID_TABLE SET UUID = :1 WHERE REFERENCE = :2"
                cursor.execute(update_query, (uuid_value, reference))
            else:
                # If the reference doesn't exist, insert a new row
                insert_query = "INSERT INTO UUID_TABLE (REFERENCE, UUID) VALUES (:1, :2)"
                cursor.execute(insert_query, (reference, uuid_value))

        connection.commit()
        print("UUID updated/inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
oracle_connection = cx_Oracle.connect('your_username', 'your_password', 'your_oracle_connection_string')

references = ['user_1', 'product_42', 'order_123']
for reference in references:
    generated_uuid = generate_uuid()
    update_or_insert_uuid_to_oracle(oracle_connection, reference, generated_uuid)

# Don't forget to close the connection when you're done
oracle_connection.close()

