import psycopg2
from datetime import datetime

from enve import settings

try:
    conn = psycopg2.connect(
        host=settings.database_host,
        database=settings.database_name,
        user=settings.database_user,
        password=settings.database_password,
        port=settings.database_port
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