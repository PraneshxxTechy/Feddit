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
    votes = [
    (1, 1, 1),
    (2, 1, -1),
    (3, 2, 1),
    (4, 3, 1),
    ]

    cursor.executemany(
    """
    INSERT INTO votes (user_id, post_id, vote_type)
    VALUES (%s, %s, %s)
    """,
    votes
    )

    conn.commit()

    print("Votes inserted successfully")
except Exception as e:
    print("Error occurred:", e)
finally:
    cursor.close()
    conn.close()