import psycopg2
from datetime import datetime

from enve import settings

# connect to database
conn = psycopg2.connect(
    host=settings.database_host,
    database=settings.database_name,
    user=settings.database_user,
    password=settings.database_password,
    port=settings.database_port
)

cursor = conn.cursor()

# sample users
users = [
    ("alice", "alice@gmail.com", "pass123", datetime.now()),
    ("bob", "bob@gmail.com", "secret456", datetime.now()),
    ("charlie", "charlie@gmail.com", "charlie789", datetime.now()),
    ("david", "david@gmail.com", "davpass111", datetime.now()),
    ("emma", "emma@gmail.com", "emma222", datetime.now())
]

# insert query
insert_query = """
INSERT INTO users (username, email, password, created_at)
VALUES (%s, %s, %s, %s)
"""

# execute many inserts
cursor.executemany(insert_query, users)

# commit changes
conn.commit()

print("Sample users inserted successfully!")

cursor.close()
conn.close()