import streamlit as st

from Backend.src.routes.login import findUserById, loginUser
from Backend.src.auth.deco import SessionLocal
from Backend.src.services.utils import change_password_dialog

db = SessionLocal()

#TODO: on login attach databse call to validate user and if user name is admin or role is assigned admin then we move to admin page
def login_page_logic():
    try:
        left_co, cent_co, last_co = st.columns(spec=[2.9, 3.9, 0.6], vertical_alignment="center")

        with cent_co:
            with st.container(width= 300):
                st.title("Login Page")
                username = st.text_input("Username", placeholder="user@mail.com", label_visibility="collapsed")

                password = st.text_input("Password", type="password", placeholder="******",
                                         label_visibility="collapsed")

                col1, _, col2  = st.columns([1.3,0.1,1.8])

                login_clicked = col1.button("Login", use_container_width=True)
                change_pw_clicked = col2.button("Change Password", type="secondary", use_container_width=True)

            if login_clicked:
                if not username or not password:
                    st.warning("Please enter both fields.")
                else:
                    with SessionLocal() as db_session:
                        api_res = loginUser(username, password, db_session)

                    if api_res.get("role") != 'admin':
                        st.warning('Login through Admin Credential', width=300)
                    elif api_res.get("status"):
                        st.session_state.logged_in = True
                        st.session_state.user_email = username
                        st.session_state.id = api_res["user_id"]
                        st.session_state.role = api_res.get("role")
                        st.session_state.set_cookie_now = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

            if change_pw_clicked:
                change_password_dialog()
    except Exception as e:
        # Use st.error so you see the error on the webpage while debugging
        st.error(f"Error at function {login_page_logic.__name__} : {e}")