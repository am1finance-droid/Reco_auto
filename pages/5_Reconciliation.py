import streamlit as st
import pandas as pd
from io import BytesIO

from modules.reconciliation.reconciliation_engine import (
    get_vendor_mapping,
    read_vendor_statement,
    standardize_vendor_statement,
    standardize_books_ledger,
    create_amount_column,
    reconcile_amount,
    get_unmatched_records,
)

from modules.reconciliation.reconciliation_history import (
    save_reconciliation_run
)

from modules.masters.vendor_master import (
    get_all_vendors
)

# ----------------------------------
# Login Check
# ----------------------------------

if not st.session_state.get(
        "logged_in",
        False
):
    st.switch_page("app.py")

# ----------------------------------
# Page Title
# ----------------------------------

st.title("🔄 Reconciliation")

# ----------------------------------
# Vendor List
# ----------------------------------

vendors = get_all_vendors()

vendor_dict = {}

for v in vendors:

    vendor_dict[
        f"{v['vendor_code']} - {v['vendor_name']}"
    ] = v["vendor_id"]

# ----------------------------------
# Inputs
# ----------------------------------

vendor_name = st.selectbox(
    "Vendor",
    list(vendor_dict.keys())
)

books_file = st.file_uploader(
    "Upload Books Ledger",
    type=["xlsx"]
)

statement_file = st.file_uploader(
    "Upload Vendor Statement",
    type=["xlsx"]
)

run_btn = st.button(
    "🚀 Run Reconciliation"
)

# ----------------------------------
# Run Reconciliation
# ----------------------------------

if run_btn:

    if books_file is None:

        st.error(
            "Please upload Books Ledger file"
        )

        st.stop()

    if statement_file is None:

        st.error(
            "Please upload Vendor Statement file"
        )

        st.stop()

    try:

        # ----------------------------------
        # Vendor Mapping
        # ----------------------------------

        vendor_id = vendor_dict[
            vendor_name
        ]

        mapping = get_vendor_mapping(
            vendor_id
        )

        if mapping is None:

            st.error(
                f"No Column Mapping Found For Vendor ID {vendor_id}"
            )

            st.stop()

        st.success(
            "Vendor Mapping Loaded Successfully"
        )

        # ----------------------------------
        # Books Ledger
        # ----------------------------------

        books_df = pd.read_excel(
            books_file
        )

        st.subheader(
            "Books Data Preview"
        )

        st.dataframe(
            books_df.head(10),
            use_container_width=True
        )

        books_df = standardize_books_ledger(
            books_df
        )

        books_df = create_amount_column(
            books_df
        )

        # ----------------------------------
        # Vendor Statement
        # ----------------------------------

        statement_df = read_vendor_statement(
            statement_file,
            mapping
        )

        st.subheader(
            "Original Vendor Statement"
        )

        st.dataframe(
            statement_df.head(10),
            use_container_width=True
        )

        standard_df = standardize_vendor_statement(
            statement_df,
            mapping
        )

        standard_df = create_amount_column(
            standard_df
        )

        st.subheader(
            "Standardized Statement"
        )

        st.dataframe(
            standard_df.head(10),
            use_container_width=True
        )

        # ----------------------------------
        # Reconciliation
        # ----------------------------------

        matched_df = reconcile_amount(
            books_df,
            standard_df
        )

        unmatched_df = get_unmatched_records(
            books_df,
            matched_df
        )

        # ----------------------------------
        # Summary
        # ----------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Books Records",
                len(books_df)
            )

        with col2:

            st.metric(
                "Statement Records",
                len(standard_df)
            )

        with col3:

            st.metric(
                "Matched Records",
                len(matched_df)
            )

        with col4:

            st.metric(
                "Unmatched Records",
                len(unmatched_df)
            )

        # ----------------------------------
        # Match Percentage
        # ----------------------------------

        if len(books_df) > 0:

            match_percent = round(
                (
                    len(matched_df)
                    /
                    len(books_df)
                ) * 100,
                2
            )

            st.metric(
                "Match %",
                f"{match_percent}%"
            )

            save_reconciliation_run(
                vendor_id,
                len(books_df),
                len(standard_df),
                len(matched_df),
                len(unmatched_df),
                match_percent
            )
        
        # ----------------------------------
        # Matched Records
        # ----------------------------------

        st.subheader(
            "✅ Matched Records"
        )

        st.dataframe(
            matched_df,
            use_container_width=True
        )

        # ----------------------------------
        # Unmatched Records
        # ----------------------------------

        st.subheader(
            "❌ Unmatched Records"
        )

        st.dataframe(
            unmatched_df,
            use_container_width=True
        )

        # ----------------------------------
        # Excel Download
        # ----------------------------------

        output = BytesIO()

        with pd.ExcelWriter(
                output,
                engine="openpyxl"
        ) as writer:

            matched_df.to_excel(
                writer,
                sheet_name="Matched",
                index=False
            )

            unmatched_df.to_excel(
                writer,
                sheet_name="Unmatched",
                index=False
            )

        output.seek(0)

        st.download_button(
            label="📥 Download Reconciliation Report",
            data=output,
            file_name="Reconciliation_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success(
            "Reconciliation Completed Successfully"
        )

    except Exception as e:

        st.error(
            f"Error : {str(e)}"
        )