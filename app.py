import streamlit as st
import extra_streamlit_components as cookie_manager
from UI.utils.login_page import login_page_logic
from UI.views.AdminPage import admin_page_logic
from UI.views.HomePage import homepage

st.set_page_config(page_title="Email Project", page_icon="📦", layout="wide")

controller = cookie_manager.CookieManager()

submit_button_flag = False


if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "page" not in st.session_state:
    st.session_state.page = "login"

if "view_email_count" not in st.session_state:
    st.session_state.view_email_count = 0


def show_login():
    try:
        login_page_logic()

        if st.session_state.get("logged_in"):
            if st.session_state.get("role") == "admin":
                st.session_state.page = "admin"
            else:
                st.session_state.page = "home"

            st.rerun()

    except Exception as e:
        print(f"Login error: {e}")


def logout():
    print("from app - logout function")

    # ✅ Step 1: Try deleting cookie safely
    try:
        controller.delete(cookie="auth_user_token")
    except Exception as e:
        print(f"Cookie delete skipped: {e}")

    # ✅ Step 2: ALWAYS clear session
    st.session_state.clear()

    # ✅ Step 3: Reset required keys
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"

    # ✅ Step 4: Force rerun
    st.rerun()

def show_navbar():
    col1, col2, col3 = st.columns([1, 8, 1])
    role = st.session_state.get("role")
    if role == "admin":
        with col1:
            if st.button("🛠 Admin"):
                st.session_state.page = "admin"

    else:  # normal user
        with col1:
            if st.button("🏠 Home"):
                st.session_state.page = "home"

    # ✅ Logout always visible
    with col3:
        if st.button("🚪 Logout"):
            logout()
            st.stop()


if not st.session_state.logged_in:
    show_login()
else:
    # ✅ Ensure default page is set ONCE after login
    if st.session_state.page == "login":
        if st.session_state.get("role") == "admin":
            st.session_state.page = "admin"
        else:
            st.session_state.page = "home"

        st.rerun()

    show_navbar()

    # ✅ Now page will always be correct
    if st.session_state.page == "home":
        homepage()

    elif st.session_state.page == "admin":
        admin_page_logic()