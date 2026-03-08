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
    comments = [
    (1, 1, "Great post!", datetime.now()),
    (2, 1, "Thanks for sharing.", datetime.now()),
    (3, 2, "Very helpful!", datetime.now()),
    (4, 3, "Looking forward to more.", datetime.now()),
    ]

    cursor.executemany(
    """
    INSERT INTO comments (user_id, post_id, comment, created_at)
    VALUES (%s, %s, %s, %s)
    """,
    comments
    )

    conn.commit()

    print("Comments inserted successfully")
except Exception as e:
    print("Error occurred:", e)
finally:
    cursor.close()
    conn.close()