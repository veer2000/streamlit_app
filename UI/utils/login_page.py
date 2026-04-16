import streamlit as st

from Backend.src.routes.login import findUserById, loginUser
from Backend.src.auth.deco import SessionLocal
from Backend.src.services.utils import change_password_dialog, takeover_dialog

db = SessionLocal()

#TODO: on login attach databse call to validate user and if user name is admin or role is assigned admin then we move to admin page
def login_page_logic(passed_session_id):
    try:
        left_co, cent_co, last_co = st.columns(spec=[2.9, 3.9, 0.6], vertical_alignment="center")

        with cent_co:
            with st.container():
                st.title("Login to System")
                username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed", width=300)
                password = st.text_input("Password", type="password", placeholder="Enter your password",
                                         label_visibility="collapsed", width=300)

                # Create the button columns
                cent_co_left, cent_co_mid, cent_co_right = st.columns([1, 2, 2], gap="xxsmall")

                with cent_co_left:
                    # Logic inside the button

                    if st.button("Login", icon_position="right", width=100):
                        print(f'At login logic - Button Actually Pressed')
                        if not username or not password:
                            st.warning("Please enter both fields.")
                        else:
                            # 1. Check Admin
                            if username == "admin@mail.com" and password == "admin1":
                                st.session_state.logged_in = True
                                st.session_state.user_email = "admin"
                                st.session_state.role = 'admin'
                                st.session_state.set_cookie_now = True
                                st.rerun()

                            # 2. Check Database
                            with SessionLocal() as db_session:
                                api_res = loginUser(email=username, password=password, passed_session_id=passed_session_id , db=db_session)
                            print(f' printing user_name fetched from user table {api_res.get("user_name")}')
                            if api_res.get("conflict"):
                                st.session_state.show_takeover_dialog = True
                                st.session_state.pending_login = {
                                    "email": username,
                                    "password": password
                                }
                                st.stop()
                            if api_res and api_res.get("status"):
                                st.session_state.logged_in = True
                                st.session_state.user_email = username
                                st.session_state.id = api_res["user_id"]
                                st.session_state.role = api_res['role'] #'user'
                                st.session_state.set_cookie_now = True
                                st.rerun()
                            else:
                                error_detail = api_res.get("detail") if isinstance(api_res, dict) else None
                                if error_detail:
                                    st.error(error_detail)
                                else:
                                    st.error("Invalid credentials")

                with cent_co_mid:
                    # This is now OUTSIDE the login button logic,
                    # so it will always stay visible!
                    if st.button("Change Password", icon_position="left", width="content"):
                        change_password_dialog()

    except Exception as e:
        # Use st.error so you see the error on the webpage while debugging
        st.error(f"Error at function {login_page_logic.__name__} : {e}")