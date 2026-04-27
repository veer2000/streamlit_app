import streamlit as st
import extra_streamlit_components as cookie_manager
from UI.utils.login_page import login_page_logic
from UI.views.AdminPage import admin_page_logic

st.set_page_config(layout="wide")
def get_cookie_manager():
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
    try:
        if controller.get("auth_user_token"):
            controller.delete(cookie="auth_user_token")
    except Exception as e:
        print(f"Cookie delete skipped: {e}")
        raise

    st.session_state.clear()
    st.session_state.logged_in = False
    st.session_state["page"] = "login"

    st.rerun()

def show_login():
    try:
        login_page_logic()

        if st.session_state.get("logged_in"):
            # print('inside show_login first if')
            # controller.set('auth_user_token', st.session_state.user_email, expires_at=datetime.datetime.now() + datetime.timedelta(days=1))
            if st.session_state.get("role") == "admin":
                st.session_state.page = "admin"

            st.rerun()

    except Exception as e:
        # print(f"Login error: {e}")
        raise


def show_navbar():
    col1, col2, col3 = st.columns([3, 10, 3])
    role = st.session_state.get("role")

    # ===== LEFT BUTTON =====
    if role == "admin":
        with col1:
            if st.button("Manage Priority", use_container_width=True):
                st.session_state.page = "admin"
                st.session_state.admin_tab = "manage"   # directly go to manage
    else:
        st.warning('Not Admin')

    # ===== CENTER NAV (ADMIN ONLY) =====
    if role == "admin" and st.session_state.get("page") == "admin":

        if "admin_tab" not in st.session_state:
            st.session_state.admin_tab = "manage"

        with col2:
            c1, c2, c3 = st.columns(3)

            with c1:
                if st.button("User Activity", use_container_width=True):
                    st.session_state.admin_tab = "activity"

            with c2:
                if st.button("Stats", use_container_width=True):
                    st.session_state.admin_tab = "stats"

            with c3:
                if st.button("Detailed Stats", use_container_width=True):
                    st.session_state.admin_tab = "detailed"

    # ===== RIGHT BUTTON =====
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.stop()


if not st.session_state.logged_in:
    show_login()
else:
    if st.session_state.page == "login":
        if st.session_state.get("role") == "admin":
            st.session_state.page = "admin"
        else:
            st.session_state.page = "home"

        st.rerun()
    show_navbar()

    if st.session_state.page == "admin":
        admin_page_logic()