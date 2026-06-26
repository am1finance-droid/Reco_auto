import hashlib
from database.db_connection import get_connection

def verify_password(password, stored_hash):

    return (
        hashlib.sha256(
            password.encode()
        ).hexdigest()
        == stored_hash
    )

def authenticate_user(
        username,
        password
):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=%s
        AND is_active=1
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return None

    if verify_password(
            password,
            user["password_hash"]
    ):
        return user

    return None