import streamlit as st
import pandas as pd

from modules.masters.column_mapping import (
    get_all_vendors,
    get_mapping_by_vendor,
    save_mapping,
    update_mapping
)

if not st.session_state.get(
        "logged_in",
        False
):
    st.switch_page("app.py")

st.title(
    "🗂 Column Mapping"
)

vendors = get_all_vendors()

vendor_options = {}

for vendor in vendors:

    vendor_options[
        f"{vendor['vendor_code']} - {vendor['vendor_name']}"
    ] = vendor["vendor_id"]

selected_vendor = st.selectbox(
    "Select Vendor",
    list(vendor_options.keys())
)

vendor_id = vendor_options[
    selected_vendor
]

uploaded_file = st.file_uploader(
    "Upload Sample Vendor Statement",
    type=["xlsx"]
)

if uploaded_file:

    excel_file = pd.ExcelFile(
        uploaded_file
    )

    sheet_names = excel_file.sheet_names

    selected_sheet = st.selectbox(
        "Select Sheet",
        sheet_names
    )

    header_row = st.number_input(
        "Header Row",
        min_value=1,
        value=1
    )

    sample_df = pd.read_excel(
        uploaded_file,
        sheet_name=selected_sheet,
        header=header_row - 1
    )

    columns = [
        "None"
    ] + sample_df.columns.tolist()

    st.subheader(
        "Detected Columns"
    )

    st.write(
        sample_df.columns.tolist()
    )

    existing_mapping = (
        get_mapping_by_vendor(
            vendor_id
        )
    )

    invoice_column = st.selectbox(
        "Invoice Column",
        columns
    )

    voucher_column = st.selectbox(
        "Voucher Column",
        columns
    )

    amount_column = st.selectbox(
        "Amount Column",
        columns
    )

    debit_column = st.selectbox(
        "Debit Column",
        columns
    )

    credit_column = st.selectbox(
        "Credit Column",
        columns
    )

    date_column = st.selectbox(
        "Date Column",
        columns
    )

    narration_column = st.selectbox(
        "Narration Column",
        columns
    )

    qty_column = st.selectbox(
        "Qty Column",
        columns
    )

    batch_column = st.selectbox(
        "Batch Column",
        columns
    )

    bp_no_column = st.selectbox(
        "BP No Column",
        columns
    )

    period_column = st.selectbox(
        "Period Column",
        columns
    )

    if st.button(
            "💾 Save Mapping"
    ):

        if existing_mapping:

            update_mapping(
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
                selected_sheet,
                header_row
            )

            st.success(
                "Mapping Updated Successfully"
            )

        else:

            save_mapping(
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
                selected_sheet,
                header_row
            )

            st.success(
                "Mapping Saved Successfully"
            )

    st.subheader(
        "Sample Data"
    )

    st.dataframe(
        sample_df.head(10)
    )