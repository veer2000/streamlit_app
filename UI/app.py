import streamlit as st

st.set_page_config(page_title="My App", page_icon="🔐", layout="wide")

#NOTE: what actually are we doing here session_state is a json or dictionay like inerface and why we use it we use it to store/presist variable accorss script run
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 2. Main Page Content
st.title("Welcome to out app",text_alignment="center")
st.markdown("---")

def login_page():
    # st.title("Login to System",text_alignment="center")
    try:
        # NOTE: below code is used for adding vertical spaceing kind of customized space we are just creating column here we have created 3 column and we are using center one
        left_co, cent_co, last_co = st.columns(spec=[2.1, 3, 1],vertical_alignment="center")
        lef_bu, ce_bu, ri_bu = st.columns([3.1, 2, 2.9],vertical_alignment="center")
        with cent_co:
            st.title("Login to System")
            username = st.text_input("Username",placeholder="Enter your username", width=300, label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Enter your password", width=300, label_visibility="collapsed")

        with ce_bu:
            login_button = st.button("Login", icon_position="right", width=200)
    except Exception as e:
        print(f'Error at function {login_page.__name__} error : {e}')

def home_page():
    try:
        st.title("Home Page")
    except Exception as e:
        print(f'Error at {home_page.__name__} error : {e}')

# st.write("This is the main 'Home' page of your application.")
# st.write("You can navigate between the different pages using the sidebar on the left.")


# Pro-tip: You can add common elements here that should appear on all pages
st.sidebar.success("Select a page above.")
if not st.session_state.logged_in:
    login_page()
else:
    home_page()