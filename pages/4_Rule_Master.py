import streamlit as st
import pandas as pd

from modules.masters.vendor_master import (
    get_all_vendors
)

from modules.masters.rule_master import (
    add_rule,
    get_all_rules,
    get_modules
)

if not st.session_state.get(
        "logged_in",
        False
):
    st.switch_page("app.py")

st.title("⚙ Rule Master")

# -----------------------------------
# Success Message
# -----------------------------------

if st.session_state.get(
        "rule_saved",
        False
):

    st.success(
        "✅ Rule Saved Successfully"
    )

    del st.session_state[
        "rule_saved"
    ]

# -----------------------------------
# Load Modules
# -----------------------------------

modules = get_modules()

module_dict = {}

for m in modules:

    module_dict[
        m["module_name"]
    ] = m["module_id"]

# -----------------------------------
# Load Vendors
# -----------------------------------

vendors = get_all_vendors()

vendor_dict = {}

for v in vendors:

    vendor_dict[
        f"{v['vendor_code']} - {v['vendor_name']}"
    ] = v["vendor_id"]

# -----------------------------------
# Match Fields
# -----------------------------------

field_options = [
    "",
    "invoice_no",
    "voucher_no",
    "amount",
    "date",
    "qty",
    "batch_no",
    "bp_no",
    "period"
]

# -----------------------------------
# Rule Form
# -----------------------------------

with st.form("rule_form"):

    col1, col2 = st.columns(2)

    with col1:

        selected_module = st.selectbox(
            "Module",
            list(module_dict.keys())
        )

        vendor_name = st.selectbox(
            "Vendor",
            list(vendor_dict.keys())
        )

        rule_name = st.text_input(
            "Rule Name"
        )

    with col2:

        tolerance_amount = st.number_input(
            "Tolerance Amount",
            value=0.00
        )

        priority_no = st.number_input(
            "Priority",
            min_value=1,
            value=1
        )

        active_flag = st.checkbox(
            "Active",
            value=True
        )

    st.divider()

    col3, col4, col5 = st.columns(3)

    with col3:

        match_field_1 = st.selectbox(
            "Match Field 1",
            field_options
        )

    with col4:

        match_field_2 = st.selectbox(
            "Match Field 2",
            field_options
        )

    with col5:

        match_field_3 = st.selectbox(
            "Match Field 3",
            field_options
        )

    save_btn = st.form_submit_button(
        "💾 Save Rule"
    )

# -----------------------------------
# Save Rule
# -----------------------------------

if save_btn:

    if rule_name.strip() == "":

        st.error(
            "Rule Name Required"
        )

    else:

        add_rule(
            module_dict[selected_module],
            vendor_dict[vendor_name],
            rule_name,
            match_field_1,
            match_field_2,
            match_field_3,
            tolerance_amount,
            priority_no,
            active_flag=1 if active_flag else 0
        )

        st.session_state[
            "rule_saved"
        ] = True

        st.rerun()

# -----------------------------------
# Rule List
# -----------------------------------

st.divider()

st.subheader(
    "Rule List"
)

rules = pd.DataFrame(
    get_all_rules()
)

if not rules.empty:

    search_text = st.text_input(
        "🔍 Search Rule"
    )

    if search_text:

        rules = rules[
            rules["rule_name"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        rules,
        use_container_width=True
    )

else:

    st.info(
        "No Rules Found"
    )