import csv

def append_to_csv(file_path, data):
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        print("Data appended successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = 'example.csv'
data_to_append = ['John', 'Doe', 25, 'john.doe@email.com']

append_to_csv(file_path, data_to_append)

import csv
import uuid
import os

def generate_uuid(reference):
    return str(uuid.uuid4())

def append_uuid_to_csv(file_path, reference, uuid_value):
    try:
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            # If the file is new, write header
            if not file_exists:
                writer.writerow(['Reference', 'UUID'])

            writer.writerow([reference, uuid_value])
        print("UUID appended successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = 'uuid_records.csv'

references = ['user_1', 'product_42', 'order_123']
for reference in references:
    generated_uuid = generate_uuid(reference)
    append_uuid_to_csv(file_path, reference, generated_uuid)

import csv
import uuid
import os

def generate_uuid():
    return str(uuid.uuid4())

def find_row_by_reference(file_path, reference):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == reference:
                    return header, row
    except FileNotFoundError:
        return None, None

def update_or_append_uuid_to_csv(file_path, reference, uuid_value):
    try:
        header, existing_row = find_row_by_reference(file_path, reference)

        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            # If the reference exists, update the row
            if existing_row:
                existing_row[1] = uuid_value
            else:
                # If the file is new, write header
                if not os.path.isfile(file_path):
                    writer.writerow(['Reference', 'UUID'])
                writer.writerow([reference, uuid_value])
                
        print("UUID updated/appended successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = 'uuid_records.csv'

references = ['user_1', 'product_42', 'order_123']
for reference in references:
    generated_uuid = generate_uuid()
    update_or_append_uuid_to_csv(file_path, reference, generated_uuid)

