import datetime

import streamlit as st
import extra_streamlit_components as cookie_manager
# from Backend.src.services.curd import logout_user_log_entry, find_user_log
from Backend.src.services.database import SessionLocal
# from Backend.src.services.utils import get_session_id, takeover_dialog
from UI.utils.login_page import login_page_logic
from UI.views.AdminPage import admin_page_logic
from UI.views.HomePage import homepage
import uuid

st.set_page_config(layout="wide")
def get_cookie_manager():
    print(f'get_cookie_manager called ')
    return cookie_manager.CookieManager()

controller = get_cookie_manager()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "submit_status" not in st.session_state:
    st.session_state.submit_status = False

if "form_change" not in st.session_state:
    st.session_state.form_change = False

if "show_warning" not in st.session_state:
    st.session_state.show_warning = False

if "pending_user" not in st.session_state:
    st.session_state.pending_user = None

def logout():
    print("from app - logout function")
    try:
        controller.delete(cookie="auth_user_token")
    except Exception as e:
        print(f"Cookie delete skipped: {e}")

    # dev_id = st.session_state.device_id
    st.session_state.clear()
    # st.session_state.device_id = dev_id
    st.session_state.logged_in = False
    st.session_state["page"] = "login"

    st.rerun()

def show_login():
    try:
        login_page_logic()

        if st.session_state.get("logged_in"):
            print('inside show_login first if')
            # controller.set('auth_user_token', st.session_state.user_email, expires_at=datetime.datetime.now() + datetime.timedelta(days=1))
            if st.session_state.get("role") == "admin":
                st.session_state.page = "admin"
            else:
                st.session_state.page = "home"

            st.rerun()

    except Exception as e:
        print(f"Login error: {e}")


def show_navbar():
    col1, col2, col3 = st.columns([1, 8, 1])
    role = st.session_state.get("role")
    if role == "admin":
        admin_page_nav_button = []
        with col1:
            if st.button("🛠 Admin",width="stretch"):
                st.session_state.page = "admin"
                if "admin_tab" not in st.session_state:
                    st.session_state.admin_tab = "manage"
    else:  # normal user
        with col1:
            if st.button("🏠 Home"):
                st.session_state.page = "home"

    if role == "admin" and st.session_state.get("page") == "admin":

        if "admin_tab" not in st.session_state:
            st.session_state.admin_tab = "manage"

        with col2:
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                if st.button("Manage Priority", use_container_width=True):
                    st.session_state.admin_tab = "manage"

            with c2:
                if st.button("User Activity", use_container_width=True):
                    st.session_state.admin_tab = "activity"

            with c3:
                if st.button("Stats", use_container_width=True):
                    st.session_state.admin_tab = "stats"

            with c4:
                if st.button("Detailed Stats", use_container_width=True):
                    st.session_state.admin_tab = "detailed"

    with col3:
        if st.button("🚪 Logout"):
            logout()
            st.stop()


print(f'lets check what is in {st.session_state.logged_in}')
if not st.session_state.logged_in:
    show_login()
else:
    print('at else part of not st.session_state.logged_in')
    if st.session_state.page == "login":
        if st.session_state.get("role") == "admin":
            st.session_state.page = "admin"
        else:
            st.session_state.page = "home"

        st.rerun()
    show_navbar()
    if st.session_state.page == "home":
        homepage()

    elif st.session_state.page == "admin":
        admin_page_logic()