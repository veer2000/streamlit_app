import datetime

import streamlit as st
import extra_streamlit_components as cookie_manager
from Backend.src.services.curd import logout_user_log_entry, find_user_log
from Backend.src.services.database import SessionLocal
from Backend.src.services.utils import get_session_id, takeover_dialog
from UI.utils.login_page import login_page_logic
from UI.views.AdminPage import admin_page_logic
from UI.views.HomePage import homepage
import uuid


st.set_page_config(page_title="Email Project", page_icon="📦", layout="wide")

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

# cookie_device_id = controller.get("device_id")

# if "device_id" not in st.session_state:
#     temp_id = str(uuid.uuid4())
#     print(f"[INIT] Temporary device_id: {temp_id}")
#     st.session_state.device_id = temp_id

# cookie_device_id = controller.get("device_id")

# if cookie_device_id:
#     if st.session_state.device_id != cookie_device_id:
#         print(f"[SYNC] Overriding session with cookie: {cookie_device_id}")
#         st.session_state.device_id = cookie_device_id
# else:
#     if "cookie_written" not in st.session_state:
#         print(f"[SYNC] Writing cookie: {st.session_state.device_id}")
#
#         controller.set(
#             "device_id",
#             st.session_state.device_id,
#             expires_at=datetime.datetime.now() + datetime.timedelta(days=365)
#         )
#
#         st.session_state.cookie_written = True
#
# device_id = st.session_state.device_id

# if not device_id:
#     print(f'device_id not found {device_id} hence generating new')
#     device_id = str(uuid.uuid4())
#     # Set a long-lived cookie (1 year) to identify this browser instance
#     controller.set('device_id', device_id, expires_at=datetime.datetime.now() + datetime.timedelta(days=365))


# print(f' device id {device_id} and sessionid is {session_id}')
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#
# if "page" not in st.session_state:
#     st.session_state.page = "login"

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

def validate_session(db_sess, email, passed_session_id):
    # session_id = get_session_id()

    user_log = find_user_log(db_sess, email)

    if not user_log:
        return False

    if user_log.session_id != passed_session_id:
        return False

    if not user_log.is_logged_in:
        return False
    return True


def show_login(passed_session_id):
    try:
        login_page_logic(passed_session_id=passed_session_id)

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
    with SessionLocal() as db_session:
        if st.session_state.role == 'user':
                logout_user_log_entry(db=db_session, user_email=st.session_state.user_email, type='user')
        else:
                logout_user_log_entry(db=db_session, user_email=st.session_state.user_email, type='admin')

    try:
        controller.delete(cookie="auth_user_token")
    except Exception as e:
        print(f"Cookie delete skipped: {e}")

    # dev_id = st.session_state.device_id
    st.session_state.clear()
    # st.session_state.device_id = dev_id
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


if st.session_state.get("show_takeover_dialog"):
    takeover_dialog()

if not st.session_state.logged_in:
    show_login(passed_session_id = session_id)
else:
    print('at else part of not st.session_state.logged_in')
    with SessionLocal() as db:
        print(' inside with of part of not st.session_state.logged_in')
        valid = validate_session(
            db_sess = db,
            email = st.session_state.user_email,
            passed_session_id= session_id
        )
        print(f'valid is {valid}')

    if not valid:
        st.warning("Session Exist's in another tab")
        logout()   # clears session + cookie
        st.stop()
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