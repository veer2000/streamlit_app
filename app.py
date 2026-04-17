import datetime

import streamlit as st
import extra_streamlit_components as cookie_manager
from Backend.src.services.curd import logout_user_log_entry, find_user_log
from Backend.src.services.database import SessionLocal
from Backend.src.services.utils import get_session_id, validate_session
from UI.utils.login_page import login_page_logic
from UI.views.AdminPage import admin_page_logic
from UI.views.HomePage import homepage
import uuid


st.set_page_config(page_title="Email Project", page_icon="📦", layout="wide")


@st.dialog("⚠️ Active Session Found")
def takeover_dialog():
    try:
        st.warning("You are already logged in in another tab.")

        col1, col2 = st.columns(2)
        st.session_state.session_id = str(uuid.uuid4())
        with col1:
            if st.button("Take Over"):
                email = st.session_state.pending_login["email"]
                role = st.session_state.get("role", "user")

                with SessionLocal() as db_session:
                    logout_user_log_entry(db_session, email, role)

                    user_log = find_user_log(db_session, email)

                    if user_log:
                        user_log.session_id = st.session_state.session_id
                        user_log.is_logged_in = True
                        user_log.log_out_time = None

                        db_session.commit()

                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.show_takeover_dialog = False

                # 🔥 IMPORTANT
                st.session_state.session_id = str(uuid.uuid4())

                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.show_takeover_dialog = False
                logout()
                st.rerun()

    except Exception as e:
        st.error(f"Error in takeover_dialog: {e}")


if st.session_state.get("show_takeover_dialog"):
    takeover_dialog()
    st.stop()


# @st.cache_resource
def get_cookie_manager():
    print(f'get_cookie_manager called ')
    return cookie_manager.CookieManager()

controller = get_cookie_manager()
if "session_id" not in st.session_state:
    st.session_state.session_id = get_session_id()
    print(f'session id is {st.session_state.session_id}')

session_id = st.session_state.session_id
# print(f'session id is {session_id}')
auth_token = controller.get('auth_user_token')


if "pending_login" not in st.session_state:
    st.session_state.pending_login = {"email": None}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"

if "view_email_count" not in st.session_state:
    st.session_state.view_email_count = 0

if not st.session_state.logged_in and auth_token:
    # NOTE: we will add a DB check here now i am just testing hence kept direct assignment
    st.session_state.logged_in = True
    st.session_state.user_email = auth_token
    # Note: You might need to fetch the 'role' from DB here if not in session
    if "role" not in st.session_state:
        st.session_state.role = "user" # Default or fetch from DB

#
# if st.session_state.get("show_takeover_dialog"):
#     print(f'first if in main')
#     with SessionLocal() as db_session:
#         takeover_dialog()

def show_login(controller_ob, passed_session_id):
    try:
        login_page_logic(controller_ob, passed_session_id=passed_session_id, )

        if st.session_state.get("logged_in"):
            controller.set('auth_user_token', st.session_state.user_email, expires_at=datetime.datetime.now() + datetime.timedelta(days=1))
            if st.session_state.get("role") == "admin":
                st.session_state.page = "admin"
            else:
                st.session_state.page = "home"

            st.rerun()

    except Exception as e:
        print(f"Login error: {e}")



def logout():
    print("from app - logout function")

    # Use .get() to avoid the AttributeError/KeyError
    user_email = st.session_state.get("user_email")
    user_role = st.session_state.get("role", "user")  # Default to 'user' if role is missing

    # Only run DB logic if we have an email
    if user_email:
        try:
            with SessionLocal() as db_session:
                logout_user_log_entry(
                    db=db_session,
                    user_email=user_email,
                    type_is=user_role
                )
        except Exception as e:
            print(f"DB Logout entry failed: {e}")

    try:
        controller.delete(cookie="auth_user_token")
    except Exception as e:
        print(f"Cookie delete skipped: {e}")

    # Clear and reset state safely
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

    with col3:
        if st.button("🚪 Logout"):
            logout()
            st.stop()




if not st.session_state.logged_in:
    show_login(controller_ob=controller, passed_session_id=session_id)
else:
    print('at else part of not st.session_state.logged_in')

    with SessionLocal() as db:
        valid = validate_session(
            db_sess=db,
            email=st.session_state.user_email,
            passed_session_id=session_id
        )

    if not valid:
        st.warning("Session Exists in another tab")

        st.session_state.show_takeover_dialog = True

        if "pending_login" not in st.session_state:
            st.session_state.pending_login = {
                "email": st.session_state.user_email
            }

        st.stop()
    if st.session_state.page == "login":
        if st.session_state.get("role") == "admin":
            st.session_state.page = "admin"
        else:
            st.session_state.page = "home"

        st.rerun()

    show_navbar()

    if st.session_state.page == "home":
        # print(f'from home st.session_state.role = {st.session_state.role}')
        homepage()

    elif st.session_state.page == "admin":
        # print(f'from admin st.session_state.role = {st.session_state.role}')
        admin_page_logic()