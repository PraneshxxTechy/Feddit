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