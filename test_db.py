from database.db_connection import (
    get_connection
)

try:

    conn = get_connection()

    print(
        "Database Connected Successfully"
    )

    conn.close()

except Exception as e:

    print(
        "Connection Error :",
        e
    )