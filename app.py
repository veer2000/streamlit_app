import streamlit as st

st.set_page_config(page_title="Product Manager", page_icon="📦")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    # st.title("Login to System",text_alignment="center")
    try:
        # NOTE: below code is used for adding vertical spaceing kind of customized space we are just creating column here we have created 3 column and we are using center one
        left_co, cent_co, last_co = st.columns(spec=[2.1, 3, 1],vertical_alignment="center")
        lef_bu, ce_bu, ri_bu = st.columns([3.1, 2, 2.2],vertical_alignment="center")
        with cent_co:
            st.title("Login to System")
            username = st.text_input("Username",placeholder="Enter your username", width=300, label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Enter your password", width=300, label_visibility="collapsed")

        with ce_bu:
            if st.button("Login", icon_position="right", width=200):
                if username == "admin" and password == "admin1":
                    st.session_state.logged_in = True
                    st.success("Logged in")
                    st.rerun()
                else:
                    st.error("Incorrect username or password")


    except Exception as e:
        print(f'Error at function {login_page.__name__} error : {e}')

def logout():
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login_page, title="Login", icon="🔒", default=(not st.session_state.logged_in))
home_page = st.Page("UI/views/01_HomePage.py", title="Home", icon="🏠", default=st.session_state.logged_in)
data_page = st.Page("UI/views/page_1.py", title="Data View", icon="📊")
report_page = st.Page("UI/views/page_2.py", title="Reports", icon="📄")

# --- 4. NAVIGATION LOGIC ---
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
    # Before login: Navigation ONLY contains the login page
    # This effectively removes the sidebar navigation entirely
    pg = st.navigation([login_page], position="hidden")

# --- 5. RUN NAVIGATION ---
pg.run()