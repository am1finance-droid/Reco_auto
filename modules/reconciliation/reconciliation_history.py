from database.db_connection import get_connection


def save_reconciliation_run(
        vendor_id,
        total_books,
        total_statement,
        matched_count,
        unmatched_count,
        match_percentage
):

    conn = get_connection()

    if conn is None:
        raise Exception("Database connection is None")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reconciliation_runs
        (
            vendor_id,
            total_books,
            total_statement,
            matched_count,
            unmatched_count,
            match_percentage
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s
        )
        """,
        (
            vendor_id,
            total_books,
            total_statement,
            matched_count,
            unmatched_count,
            match_percentage
        )
    )

    conn.commit()

    conn.close()

    def get_reconciliation_history():

        conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT
            r.run_id,
            v.vendor_name,
            r.total_books,
            r.total_statement,
            r.matched_count,
            r.unmatched_count,
            r.match_percentage,
            r.created_at
        FROM reconciliation_runs r
        INNER JOIN vendors v
            ON r.vendor_id = v.vendor_id
        ORDER BY r.run_id DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data