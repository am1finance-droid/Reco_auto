import hashlib

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def verify_password(
        entered_password,
        stored_hash
):

    return (
        hash_password(
            entered_password
        )
        == stored_hash
    )