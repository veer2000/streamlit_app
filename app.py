import streamlit as st

st.set_page_config(page_title="Product Manager", page_icon="📦", layout="wide")

from UI.utils.login_page import login_page_logic

if not st.session_state.get("logged_in", False):
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page_model():
    try:
        login_page_logic()
    except Exception as e:
        print(f'Error at function {login_page_model.__name__} error : {e}')

def logout():
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login_page_model, title="Login", icon="🔒", default=(not st.session_state.logged_in))
home_page = st.Page("UI/views/01_HomePage.py", title="Home", icon="🏠", default=st.session_state.logged_in)
data_page = st.Page("UI/views/page_1.py", title="Data View", icon="📊")
report_page = st.Page("UI/views/page_2.py", title="Reports", icon="📄")

#NOTE: Below part is for Navigation if you remove things from "Main" those will not be shown in UI and it is also has sidebar logic
if st.session_state.logged_in:
    # After login: Define the sidebar navigation
    pg = st.navigation(
        {
            "Main": [home_page,data_page,report_page],
            # "Tools": [data_page],
            # "Account": []
        }
    )
    # Show the logout button in the sidebar
    logout()
else:
    #NOTE: Before login: Navigation ONLY contains the login page This effectively removes the sidebar navigation entirely
    pg = st.navigation([login_page], position="hidden")

# NOTE: this is trigger point of application
pg.run()