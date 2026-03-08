import psycopg2
from datetime import datetime

# connect to database
conn = psycopg2.connect(
    host="localhost",
    database="reddit",
    user="postgres",
    password="pranesh@8917",
    port=5432
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