from datetime import datetime, timedelta
from streamlit_quill import st_quill
import streamlit as st
import extra_streamlit_components as cookie_manager
from UI.utils.login_page import login_page_logic



st.set_page_config(page_title="Product Manager", page_icon="📦", layout="wide")

controller = cookie_manager.CookieManager()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
# NOTE: need to work on session management
# saved_user = controller.get(cookie="auth_user_token")
# if saved_user and not st.session_state.logged_in:
#     st.session_state.logged_in = True
#     st.session_state.user_email = saved_user

if st.session_state.get("set_cookie_now"):
    controller.set(
        cookie="auth_user_token",
        val=st.session_state.user_email,
        expires_at=datetime.now() + timedelta(days=1)
    )
    # Clear the flag so it doesn't keep setting it
    del st.session_state["set_cookie_now"]
#
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

def logout():
    if st.sidebar.button("Log out"):
        controller.delete(cookie="auth_user_token")
        st.session_state.logged_in = False
        st.session_state.clear()
        st.rerun()

login_page = st.Page(login_page_model, title="Login", icon="🔒", default=(not st.session_state.logged_in))
home_page = st.Page("UI/views/01_HomePage.py", title="Home", icon="🏠", default=st.session_state.logged_in)
data_page = st.Page("UI/views/page_1.py", title="Data View", icon="📊")
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

    pg = st.navigation(
        {
            "Main": [home_page,data_page,report_page],
            # "Tools": [data_page],
            # "Account": []
        }
    )

    logout()
else:
    #NOTE: Before login: Navigation ONLY contains the login page This effectively removes the sidebar navigation entirely
    pg = st.navigation([login_page], position="hidden")

# NOTE: this is trigger point of application
pg.run()