from database.db_connection import get_connection


def get_modules():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            module_id,
            module_name
        FROM reconciliation_modules
        WHERE active_flag = 1
        ORDER BY module_name
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_all_rules():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            r.*,
            m.module_name,
            v.vendor_name
        FROM reconciliation_rules r
        LEFT JOIN reconciliation_modules m
            ON r.module_id = m.module_id
        LEFT JOIN vendors v
            ON r.vendor_id = v.vendor_id
        ORDER BY r.rule_name
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def add_rule(
        module_id,
        vendor_id,
        rule_name,
        match_field_1,
        match_field_2,
        match_field_3,
        tolerance_amount,
        priority_no,
        active_flag
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reconciliation_rules
        (
            module_id,
            vendor_id,
            rule_name,
            match_field_1,
            match_field_2,
            match_field_3,
            tolerance_amount,
            priority_no,
            active_flag,
            created_at
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()
        )
        """,
        (
            module_id,
            vendor_id,
            rule_name,
            match_field_1,
            match_field_2,
            match_field_3,
            tolerance_amount,
            priority_no,
            active_flag
        )
    )

    conn.commit()

    conn.close()