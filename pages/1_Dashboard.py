import streamlit as st

from modules.reconciliation.reconciliation_history import (
    get_reconciliation_history
)

if not st.session_state.get(
        "logged_in",
        False
):
    st.switch_page("app.py")

st.title("📊 Dashboard")

st.success(
    f"Welcome {st.session_state.username}"
)

st.write(
    f"Role : {st.session_state.role}"
)

# -------------------------
# KPI Cards
# -------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Vendors",
    "0"
)

col2.metric(
    "Mappings",
    "0"
)

col3.metric(
    "Rules",
    "0"
)

col4.metric(
    "Users",
    "1"
)

st.divider()

st.subheader(
    "Quick Actions"
)
st.page_link(
    "pages/3_Column_Mapping.py",
    label="🗂 Column Mapping"
)
st.page_link(
    "pages/4_Rule_Master.py",
    label="⚙ Rule Master"
)
st.page_link(
    "pages/5_Reconciliation.py",
    label="🔄 Reconciliation"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.page_link(
        "pages/2_Vendor_Master.py",
        label="🏢 Vendor Master"
    )

with c2:
    st.page_link(
        "pages/6_Master_Setup.py",
        label="🗂 Column Mapping"
    )

with c3:
    st.page_link(
        "pages/6_Master_Setup.py",
        label="⚙ Rule Master"
    )

st.divider()


if st.button("🚪 Logout"):

    st.session_state.clear()

    st.switch_page("app.py")

import pandas as pd

history_df = pd.DataFrame(
    get_reconciliation_history()
)

st.subheader(
    "Recent Reconciliation Runs"
)

st.dataframe(
    history_df,
    use_container_width=True
)