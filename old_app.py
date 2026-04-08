from datetime import datetime, timedelta
from streamlit_quill import st_quill
import streamlit as st
import extra_streamlit_components as cookie_manager
from UI.utils.login_page import login_page_logic
from UI.views.AdminPage import admin_page_logic
from UI.views.HomePage import  homepage

st.set_page_config(page_title="Product Manager", page_icon="📦", layout="wide")

controller = cookie_manager.CookieManager()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "view_email_count" not in st.session_state:
    st.session_state.view_email_count = 0

if not st.session_state.get("logged_in", False):
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

def login_page_model():
    try:
        login_page_logic()
    except Exception as e:
        print(f'Error at function {login_page_model.__name__} error : {e}')


def admin_page_model():
    try:
        admin_page_logic()
    except Exception as e:
        print(f'Error at function {admin_page_model.__name__} error : {e}')
        raise

def logout():
    if st.sidebar.button("Log out"):
        controller.delete(cookie="auth_user_token")
        st.session_state.clear()
        st.session_state.logged_in = False
        st.session_state.role = ''
        st.rerun()

def home_page_model():
    try:
        homepage()
    except Exception as e:
        print(f'Error at function {admin_page_model.__name__} error : {e}')
        raise

#NOTE if you want to test or login only to login page uncomment it so that on any login you only go to admin page
# st.session_state.role = 'admin'

login_page = st.Page(login_page_model, title="Login", icon="🔒")
admin_page = st.Page(admin_page_model, title="Admin") #, icon=""
home_page = st.Page(home_page_model, title="Home", icon="🏠")
report_page = st.Page("UI/views/page_2.py", title="Reports", icon="📄")

#NOTE: Below part is for Navigation if you remove things from "Main" those will not be shown in UI and it is also has sidebar logic
if st.session_state.logged_in:
    st.markdown("""
    <style>
    .main .block-container {
        display: flex;
        justify-content: center;
        height: 90vh;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.session_state.get('role') == 'admin':
        pages = {
            "Admin Control": [admin_page]
        }
    else:
        pages = {
            "Main": [home_page, report_page]
        }
    pg = st.navigation(pages,position="hidden")
    logout()
else:
    #NOTE: Before login: Navigation ONLY contains the login page This effectively removes the sidebar navigation entirely
    pg = st.navigation([login_page], position="hidden")

# NOTE: this is trigger point of application
pg.run()