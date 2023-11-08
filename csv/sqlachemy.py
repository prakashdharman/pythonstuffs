import uuid
from sqlalchemy import create_engine, Column, String, MetaData, Table
from sqlalchemy.sql import select

def generate_uuid():
    return str(uuid.uuid4())

def find_uuid_by_reference(engine, reference):
    metadata = MetaData()
    uuid_table = Table('UUID_TABLE', metadata, autoload_with=engine)
    query = select([uuid_table.c.UUID]).where(uuid_table.c.REFERENCE == reference)
    
    with engine.connect() as connection:
        result = connection.execute(query).fetchone()
        return result[0] if result else None

def update_or_insert_uuid_to_oracle(engine, reference, uuid_value):
    try:
        existing_uuid = find_uuid_by_reference(engine, reference)

        metadata = MetaData()
        uuid_table = Table('UUID_TABLE', metadata, autoload_with=engine)

        with engine.connect() as connection:
            # If the reference exists, update the UUID
            if existing_uuid:
                update_query = uuid_table.update().where(uuid_table.c.REFERENCE == reference).values(UUID=uuid_value)
                connection.execute(update_query)
            else:
                # If the reference doesn't exist, insert a new row
                insert_query = uuid_table.insert().values(REFERENCE=reference, UUID=uuid_value)
                connection.execute(insert_query)

        print("UUID updated/inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
oracle_connection_string = 'oracle://your_username:your_password@your_oracle_connection_string'
engine = create_engine(oracle_connection_string)

references = ['user_1', 'product_42', 'order_123']
for reference in references:
    generated_uuid = generate_uuid()
    update_or_insert_uuid_to_oracle(engine, reference, generated_uuid)

