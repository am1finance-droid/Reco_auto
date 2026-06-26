import streamlit as st
import pandas as pd

from modules.masters.vendor_master import (
    get_all_vendors,
    get_vendor_by_id,
    add_vendor,
    update_vendor
)

if not st.session_state.get(
        "logged_in",
        False
):
    st.switch_page("app.py")

# ----------------------------------
# Success Messages
# ----------------------------------

if st.session_state.get(
        "vendor_saved",
        False
):

    st.success(
        "✅ Vendor Saved Successfully"
    )

    del st.session_state[
        "vendor_saved"
    ]

if st.session_state.get(
        "vendor_updated",
        False
):

    st.success(
        "✅ Vendor Updated Successfully"
    )

    del st.session_state[
        "vendor_updated"
    ]

# ----------------------------------
# Page Header
# ----------------------------------

vendors = get_all_vendors()

col1, col2 = st.columns([3, 1])

with col1:
    st.title("🏢 Vendor Master")

with col2:
    st.metric(
        "Total Vendors",
        len(vendors)
    )

# ----------------------------------
# Vendor Selection
# ----------------------------------

vendor_options = {
    "New Vendor": 0
}

for vendor in vendors:

    vendor_options[
        f"{vendor['vendor_code']} - {vendor['vendor_name']}"
    ] = vendor["vendor_id"]

selected_vendor = st.selectbox(
    "Select Vendor",
    list(vendor_options.keys())
)

selected_id = vendor_options[
    selected_vendor
]

vendor_data = {}

if selected_id > 0:

    vendor_data = get_vendor_by_id(
        selected_id
    )

# ----------------------------------
# Vendor Form
# ----------------------------------

with st.form("vendor_form"):

    vendor_name = st.text_input(
        "Vendor Name *",
        value=vendor_data.get(
            "vendor_name",
            ""
        )
    )

    gst_no = st.text_input(
        "GST No",
        value=vendor_data.get(
            "gst_no",
            ""
        )
    )

    contact_person = st.text_input(
        "Contact Person",
        value=vendor_data.get(
            "contact_person",
            ""
        )
    )

    mobile_no = st.text_input(
        "Mobile No",
        value=vendor_data.get(
            "mobile_no",
            ""
        )
    )

    email = st.text_input(
        "Email",
        value=vendor_data.get(
            "email",
            ""
        )
    )

    vendor_type_list = [
        "Supplier",
        "Service Provider",
        "Transporter",
        "Contractor",
        "Other"
    ]

    selected_vendor_type = vendor_data.get(
        "vendor_type",
        "Supplier"
    )

    vendor_type = st.selectbox(
        "Vendor Type",
        vendor_type_list,
        index=vendor_type_list.index(
            selected_vendor_type
        ) if selected_vendor_type in vendor_type_list else 0
    )

    remarks = st.text_area(
        "Remarks",
        value=vendor_data.get(
            "remarks",
            ""
        )
    )

    active_flag = st.checkbox(
        "Active",
        value=bool(
            vendor_data.get(
                "active_flag",
                1
            )
        )
    )

    col_save, col_clear = st.columns(2)

    with col_save:

        if selected_id == 0:

            save_btn = st.form_submit_button(
                "💾 Save Vendor"
            )

            update_btn = False

        else:

            update_btn = st.form_submit_button(
                "✏️ Update Vendor"
            )

            save_btn = False

# ----------------------------------
# Save Vendor
# ----------------------------------

if save_btn:

    if vendor_name.strip() == "":

        st.error(
            "Vendor Name is required"
        )

    else:

        add_vendor(
            vendor_name,
            gst_no,
            contact_person,
            mobile_no,
            email,
            vendor_type,
            remarks
        )

        st.session_state[
            "vendor_saved"
        ] = True

        st.rerun()

# ----------------------------------
# Update Vendor
# ----------------------------------

if update_btn:

    if vendor_name.strip() == "":

        st.error(
            "Vendor Name is required"
        )

    else:

        update_vendor(
            selected_id,
            vendor_data["vendor_name"]
            and vendor_name,
            vendor_data["vendor_code"],
            gst_no,
            contact_person,
            mobile_no,
            email,
            vendor_type,
            remarks,
            1 if active_flag else 0
        )

        st.session_state[
            "vendor_updated"
        ] = True

        st.rerun()

# ----------------------------------
# Vendor List
# ----------------------------------

vendors = get_all_vendors()

vendors_df = pd.DataFrame(
    vendors
)

st.divider()

st.subheader(
    "Vendor List"
)

st.info(
    f"Total Vendors : {len(vendors_df)}"
)

search_text = st.text_input(
    "🔍 Search Vendor"
)

if not vendors_df.empty:

    if search_text:

        vendors_df = vendors_df[
            vendors_df[
                "vendor_name"
            ]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    display_df = vendors_df[
        [
            "vendor_code",
            "vendor_name",
            "vendor_type",
            "contact_person",
            "mobile_no",
            "active_flag"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True
    )

else:

    st.info(
        "No Vendor Found"
    )