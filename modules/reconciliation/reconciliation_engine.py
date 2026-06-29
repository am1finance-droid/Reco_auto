import pandas as pd

from database.db_connection import get_connection


def get_vendor_mapping(vendor_id):

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

    mapping = cursor.fetchone()

    conn.close()

    return mapping


def read_vendor_statement(
        uploaded_file,
        mapping
):

    sheet_name = mapping["sheet_name"]

    header_row = (
        mapping["header_row"] - 1
    )

    df = pd.read_excel(
        uploaded_file,
        sheet_name=sheet_name,
        header=header_row
    )

    return df


def standardize_vendor_statement(
        df,
        mapping
):

    rename_dict = {}

    if mapping["invoice_column"]:
        rename_dict[
            mapping["invoice_column"]
        ] = "invoice_no"

    if mapping["voucher_column"]:
        rename_dict[
            mapping["voucher_column"]
        ] = "voucher_no"

    if mapping["amount_column"]:
        rename_dict[
            mapping["amount_column"]
        ] = "amount"

    if mapping["debit_column"]:
        rename_dict[
            mapping["debit_column"]
        ] = "debit"

    if mapping["credit_column"]:
        rename_dict[
            mapping["credit_column"]
        ] = "credit"

    if mapping["date_column"]:
        rename_dict[
            mapping["date_column"]
        ] = "date"

    if mapping["narration_column"]:
        rename_dict[
            mapping["narration_column"]
        ] = "narration"

    if mapping["qty_column"]:
        rename_dict[
            mapping["qty_column"]
        ] = "qty"

    if mapping["batch_column"]:
        rename_dict[
            mapping["batch_column"]
        ] = "batch_no"

    if mapping["bp_no_column"]:
        rename_dict[
            mapping["bp_no_column"]
        ] = "bp_no"

    if mapping["period_column"]:
        rename_dict[
            mapping["period_column"]
        ] = "period"

    df = df.rename(
        columns=rename_dict
    )

    return df

    from modules.reconciliation.matcher import Matcher

    matcher = Matcher()

    matched_df = matcher.amount_match(
    books_df,
    standard_df
    )

    books_df["amount"] = pd.to_numeric(
        books_df["amount"],
        errors="coerce"
    )

    statement_df["amount"] = pd.to_numeric(
        statement_df["amount"],
        errors="coerce"
    )

    matched = books_df.merge(
        statement_df,
        on="amount",
        how="inner"
    )

    return matched


def get_unmatched_records(
        books_df,
        matched_df
):

    unmatched_df = books_df[
        ~books_df["amount"].isin(
            matched_df["amount"]
        )
    ]

    return unmatched_df

def standardize_books_ledger(
        books_df
):

    books_df = books_df.rename(
        columns={
            "DATE": "date",
            "Dr Cr": "dr_cr",
            "PARTICULARS": "narration",
            "LOCATION": "location",
            "VOUCHER TYPE": "voucher_type",
            "VOUCHER NO.": "voucher_no",
            "Debit": "debit",
            "Credit": "credit"
        }
    )

    return books_df

def create_amount_column(df):

    df["debit"] = pd.to_numeric(
        df["debit"],
        errors="coerce"
    ).fillna(0)

    df["credit"] = pd.to_numeric(
        df["credit"],
        errors="coerce"
    ).fillna(0)

    df["amount"] = df["debit"]

    df.loc[
        df["amount"] == 0,
        "amount"
    ] = df["credit"]

    return df

def standardize_books_ledger(
        books_df
):

    books_df = books_df.rename(
        columns={
            "DATE": "date",
            "Dr Cr": "dr_cr",
            "PARTICULARS": "narration",
            "LOCATION": "location",
            "VOUCHER TYPE": "voucher_type",
            "VOUCHER NO.": "voucher_no",
            "Debit": "debit",
            "Credit": "credit"
        }
    )

    return books_df    