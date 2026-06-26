import streamlit as st

tab1, tab2, tab3 = st.tabs(
    [
        "Vendor Master",
        "Column Mapping",
        "Rule Master"
    ]
)

with tab1:
    st.write("Vendor Master")

with tab2:
    st.write("Column Mapping")

with tab3:
    st.write("Rule Master")