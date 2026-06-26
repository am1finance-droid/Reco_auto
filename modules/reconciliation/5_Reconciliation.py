import streamlit as st
import pandas as pd

from modules.masters.vendor_master import (
    get_all_vendors
)

if not st.session_state.get(
        "logged_in",
        False
):
    st.switch_page("app.py")

st.title("🔄 Reconciliation")

vendors = get_all_vendors()

vendor_dict = {}

for v in vendors:

    vendor_dict[
        f"{v['vendor_code']} - {v['vendor_name']}"
    ] = v["vendor_id"]

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

if run_btn:

    st.success("Button Working")

    if books_file is None:
        st.error("Please upload Books Ledger file")
        st.stop()

    if statement_file is None:
        st.error("Please upload Vendor Statement file")
        st.stop()

    books_df = pd.read_excel(books_file)
    statement_df = pd.read_excel(statement_file)

    st.success("Files Read Successfully")

    st.subheader("Books Data Preview")

    st.dataframe(
        books_df.head(10),
        use_container_width=True
    )

    st.subheader("Statement Data Preview")

    st.dataframe(
        statement_df.head(10),
        use_container_width=True
    )