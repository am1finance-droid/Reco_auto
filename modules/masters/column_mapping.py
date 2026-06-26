from database.db_connection import get_connection


def get_all_vendors():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            vendor_id,
            vendor_name,
            vendor_code
        FROM vendors
        WHERE active_flag = 1
        ORDER BY vendor_name
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_mapping_by_vendor(
        vendor_id
):

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM vendor_column_mapping
        WHERE vendor_id=%s
        """,
        (vendor_id,)
    )

    data = cursor.fetchone()

    conn.close()

    return data


def save_mapping(
        vendor_id,
        invoice_column,
        voucher_column,
        amount_column,
        debit_column,
        credit_column,
        date_column,
        narration_column,
        qty_column,
        batch_column,
        bp_no_column,
        period_column,
        sheet_name,
        header_row
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO vendor_column_mapping
        (
            vendor_id,
            invoice_column,
            voucher_column,
            amount_column,
            debit_column,
            credit_column,
            date_column,
            narration_column,
            qty_column,
            batch_column,
            bp_no_column,
            period_column,
            sheet_name,
            header_row,
            created_at
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()
        )
        """,
        (
            vendor_id,
            invoice_column,
            voucher_column,
            amount_column,
            debit_column,
            credit_column,
            date_column,
            narration_column,
            qty_column,
            batch_column,
            bp_no_column,
            period_column,
            sheet_name,
            header_row
        )
    )

    conn.commit()

    conn.close()


def update_mapping(
        vendor_id,
        invoice_column,
        voucher_column,
        amount_column,
        debit_column,
        credit_column,
        date_column,
        narration_column,
        qty_column,
        batch_column,
        bp_no_column,
        period_column,
        sheet_name,
        header_row
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE vendor_column_mapping
        SET
            invoice_column=%s,
            voucher_column=%s,
            amount_column=%s,
            debit_column=%s,
            credit_column=%s,
            date_column=%s,
            narration_column=%s,
            qty_column=%s,
            batch_column=%s,
            bp_no_column=%s,
            period_column=%s,
            sheet_name=%s,
            header_row=%s
        WHERE vendor_id=%s
        """,
        (
            invoice_column,
            voucher_column,
            amount_column,
            debit_column,
            credit_column,
            date_column,
            narration_column,
            qty_column,
            batch_column,
            bp_no_column,
            period_column,
            sheet_name,
            header_row,
            vendor_id
        )
    )

    conn.commit()

    conn.close()