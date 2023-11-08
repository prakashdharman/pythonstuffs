def append_to_csv(file_path, data):
    try:
        with open(file_path, 'a') as file:
            line = ','.join(map(str, data)) + '\n'
            file.write(line)
        print("Data appended successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = 'example.csv'
data_to_append = ['John', 'Doe', 25, 'john.doe@email.com']

append_to_csv(file_path, data_to_append)

import uuid
import os

def generate_uuid():
    return str(uuid.uuid4())

def find_row_by_reference(file_path, reference):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip the header
                row = line.strip().split(',')
                if row[0] == reference:
                    return row
    except FileNotFoundError:
        return None

def update_or_append_uuid_to_csv(file_path, reference, uuid_value):
    try:
        existing_row = find_row_by_reference(file_path, reference)

        with open(file_path, 'a' if existing_row else 'a+', newline='') as file:
            # If the file is new, write header
            if not os.path.isfile(file_path):
                file.write('Reference,UUID\n')

            # If the reference exists, update the row
            if existing_row:
                existing_row[1] = uuid_value
                file.seek(0, os.SEEK_END)
                file.seek(file.tell() - len(line), os.SEEK_SET)
                file.write(','.join(existing_row))
            else:
                file.write(f'{reference},{uuid_value}\n')

        print("UUID updated/appended successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = 'uuid_records.csv'

references = ['user_1', 'product_42', 'order_123']
for reference in references:
    generated_uuid = generate_uuid()
    update_or_append_uuid_to_csv(file_path, reference, generated_uuid)

