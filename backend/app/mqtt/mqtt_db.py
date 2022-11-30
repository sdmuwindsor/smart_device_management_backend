from app.db import session
from sqlalchemy import text

def insert_light_value_db(device_id, brightness_val, time):
    query = f"INSERT INTO sdm.lights (device_id, brightness, created) VALUES({device_id}, {brightness_val}, '{time}')"
    with session.engine.connect() as connection:
        connection.execute(text(query))
        # connection.commit()