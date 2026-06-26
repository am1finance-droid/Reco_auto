from database.db_connection import get_connection


def get_all_vendors():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM vendors
        ORDER BY vendor_name
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_vendor_by_id(vendor_id):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM vendors
        WHERE vendor_id=%s
        """,
        (vendor_id,)
    )

    vendor = cursor.fetchone()

    conn.close()

    return vendor


def generate_vendor_code():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(vendor_id)
        FROM vendors
        """
    )

    result = cursor.fetchone()

    conn.close()

    last_id = result[0]

    if last_id is None:
        return "VEN00001"

    next_id = last_id + 1

    return f"VEN{next_id:05d}"


def add_vendor(
        vendor_name,
        gst_no,
        contact_person,
        mobile_no,
        email,
        vendor_type,
        remarks
):

    vendor_code = generate_vendor_code()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO vendors
        (
            vendor_name,
            vendor_code,
            gst_no,
            contact_person,
            mobile_no,
            email,
            vendor_type,
            remarks,
            active_flag,
            created_at
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,1,NOW()
        )
        """,
        (
            vendor_name,
            vendor_code,
            gst_no,
            contact_person,
            mobile_no,
            email,
            vendor_type,
            remarks
        )
    )

    conn.commit()

    conn.close()


def update_vendor(
        vendor_id,
        vendor_name,
        vendor_code,
        gst_no,
        contact_person,
        mobile_no,
        email,
        vendor_type,
        remarks,
        active_flag
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE vendors
        SET
            vendor_name=%s,
            vendor_code=%s,
            gst_no=%s,
            contact_person=%s,
            mobile_no=%s,
            email=%s,
            vendor_type=%s,
            remarks=%s,
            active_flag=%s,
            updated_at=NOW()
        WHERE vendor_id=%s
        """,
        (
            vendor_name,
            vendor_code,
            gst_no,
            contact_person,
            mobile_no,
            email,
            vendor_type,
            remarks,
            active_flag,
            vendor_id
        )
    )

    conn.commit()

    conn.close()