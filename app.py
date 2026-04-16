#
# from datetime import datetime, timedelta
# from streamlit_quill import st_quill
# import streamlit as st
# import extra_streamlit_components as cookie_manager
# from UI.utils.login_page import login_page_logic
# from UI.views.AdminPage import admin_page_logic
#
# st.set_page_config(page_title="Product Manager", page_icon="📦", layout="wide")
#
# controller = cookie_manager.CookieManager()
#
#
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# # NOTE: need to work on session management
# # saved_user = controller.get(cookie="auth_user_token")
# # if saved_user and not st.session_state.logged_in:
# #     st.session_state.logged_in = True
# #     st.session_state.user_email = saved_user
#
# if st.session_state.get("set_cookie_now"):
#     controller.set(
#         cookie="auth_user_token",
#         val=st.session_state.user_email,
#         expires_at=datetime.now() + timedelta(days=1)
#     )
#     # Clear the flag so it doesn't keep setting it
#     del st.session_state["set_cookie_now"]
# #
# if not st.session_state.get("logged_in", False):
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
#                 display: none;
#             }
#         </style>
#     """, unsafe_allow_html=True)
#
# def login_page_model():
#     try:
#         login_page_logic()
#     except Exception as e:
#         print(f'Error at function {login_page_model.__name__} error : {e}')
#
# def admin_page_model():
#     try:
#         admin_page_logic()
#     except Exception as e:
#         print(f'Error at function {admin_page_model.__name__} error : {e}')
#         raise
#
# def logout():
#     if st.sidebar.button("Log out"):
#         controller.delete(cookie="auth_user_token")
#         st.session_state.logged_in = False
#         st.session_state.role = ''
#         st.session_state.clear()
#         st.rerun()
#
# #NOTE if you want to test or login only to login page uncomment it so that on any login you only go to admin page
# # st.session_state.role = 'admin'
#
# login_page = st.Page(login_page_model, title="Login", icon="🔒", default=(not st.session_state.logged_in))
# # admin_page = st.Page(admin_page_model, title="Admin") #, icon=""
# home_page = st.Page("UI/views/01_HomePage.py", title="Home", icon="🏠", default=st.session_state.logged_in)
# # home_page = st.Page("UI/views/test_home_page.py", title="Home", icon="🏠", default=st.session_state.logged_in)
# admin_page = st.Page("UI/views/AdminPage.py", title="Data View", icon="📊")
# report_page = st.Page("UI/views/page_2.py", title="Reports", icon="📄")
#
# #NOTE: Below part is for Navigation if you remove things from "Main" those will not be shown in UI and it is also has sidebar logic
# if st.session_state.logged_in:
#     st.markdown("""
#     <style>
#     .main .block-container {
#         display: flex;
#         justify-content: center;
#         height: 90vh;
#     }
#     </style>
#     """, unsafe_allow_html=True)
#
#     if st.session_state.get('role') == 'admin':
#         pages = {
#             "Admin Control": [admin_page]
#         }
#     else:
#         pages = {
#             "Main": [home_page, report_page]
#         }
#     pg = st.navigation(pages)
#     logout()
#         #{
#
#             # "Admin": [admin_page],
#             # "Main": [home_page,report_page],
#             # "Tools": [admin_page],
#             # "Account": []
#         #}
#
#
# else:
#     #NOTE: Before login: Navigation ONLY contains the login page This effectively removes the sidebar navigation entirely
#     pg = st.navigation([login_page], position="hidden")
#
# # NOTE: this is trigger point of application
# pg.run()


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