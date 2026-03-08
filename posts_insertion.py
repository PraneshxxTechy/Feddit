import psycopg2
from datetime import datetime

try:
    conn = psycopg2.connect(
        host="localhost",
        database="reddit",
        user="postgres",
        password="pranesh@8917",
        port=5432
    )
    cursor = conn.cursor()
    posts = [
    (1, "Learning PostgreSQL", "PostgreSQL is powerful!", "https://example.com/postgres"),
    (2, "Python Tips", "Here are some Python tricks.", "https://example.com/python"),
    (1, "Machine Learning Basics", "ML is fascinating.", "https://example.com/ml"),
    (3, "Building APIs", "REST APIs explained.", "https://example.com/api"),
    ]

    cursor.executemany(
    """
    INSERT INTO posts (user_id, title, content, url)
    VALUES (%s, %s, %s, %s)
    """,
    posts
    )

    conn.commit()

    print("Posts inserted successfully")
except Exception as e:
    print("Error occurred:", e)
finally:
    cursor.close()
    conn.close()