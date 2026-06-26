import streamlit as st

from modules.auth.login import (
    authenticate_user
)

st.set_page_config(
    page_title="Vendor Reconciliation System",
    page_icon="📊",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------
# Login Screen
# -------------------------

if not st.session_state.logged_in:

    st.markdown(
    """
    <div style='text-align:center;padding:20px'>
        <h1>📊 Vendor Reconciliation System</h1>
        <h4>Automation & Exception Management</h4>
    </div>
    """,
    unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.subheader("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("🔐 Login"):

            user = authenticate_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user["user_id"]
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

# -------------------------
# Dashboard Redirect
# -------------------------

else:

    st.switch_page(
        "pages/1_Dashboard.py"
    )