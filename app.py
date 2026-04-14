import streamlit as st
import extra_streamlit_components as cookie_manager
from Backend.src.services.curd import logout_user_log_entry
from Backend.src.services.database import SessionLocal
from UI.utils.login_page import login_page_logic
from UI.views.AdminPage import admin_page_logic
from UI.views.HomePage import homepage

st.set_page_config(page_title="Email Project", page_icon="📦", layout="wide")

controller = cookie_manager.CookieManager()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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
    with SessionLocal() as db_session:
        logout_user_log_entry(db_session, st.session_state.user_email)

    try:
        controller.delete(cookie="auth_user_token")
    except Exception as e:
        print(f"Cookie delete skipped: {e}")

    st.session_state.clear()

    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"

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