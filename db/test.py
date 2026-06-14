from db.connection import get_connection
import os

print("HOST:", os.getenv("DB_HOST"))
print("PORT:", os.getenv("DB_PORT"))
print("DB:", os.getenv("DB_NAME"))
print("USER:", os.getenv("DB_USER"))

with get_connection() as conn:
    print("Connected:", not conn.closed)