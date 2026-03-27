import streamlit as st

from Backend.src.routes.login import findUserById, loginUser
from Backend.src.auth.deco import SessionLocal
from Backend.src.services.utils import change_password_dialog

db = SessionLocal()


def login_page_logic():
    try:
        st.markdown("""
                            <style>
                            /* This targets the main content area */
                            .main .block-container {
                                display: flex;
                                flex-direction: column;
                                justify-content: center; /* Vertical centering */
                                height: 90vh; /* Takes up 90% of the viewport height */
                            }

                            /* Optional: Make the login box itself look larger/taller */
                            [data-testid="stVerticalBlockBorderWrapper"] {
                                padding: 50px !important;
                                border-radius: 15px;
                            }
                            div.stButton > button {
                                transition: all 0.3s ease-in-out; /* Smooth transition */
                                border-radius: 8px;
                            }

                            /* 2. HOVER effect for the Login (Primary) button */
                            /* Note: Streamlit 'Primary' buttons have a specific data-testid */
                            div.stButton > button:hover {
                                background-color: #ff4b4b; /* Change to your preferred hover color */
                                color: white;
                                border-color: #ff4b4b;
                                transform: translateY(-2px); /* Slight lift effect */
                                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                            }

                            /* 3. Specific style for the 'Login' button if you use type="primary" */
                            button[kind="primary"]:hover {
                                background-color: #2e7d32 !important; /* Darker green for login success feel */
                                border-color: #2e7d32 !important;
                            }
                            </style>
                        """, unsafe_allow_html=True)

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
                        if not username or not password:
                            st.warning("Please enter both fields.")
                        else:
                            # 1. Check Admin
                            if username == "admin" and password == "admin1":
                                st.session_state.logged_in = True
                                st.rerun()

                            # 2. Check Database
                            with SessionLocal() as db_session:
                                api_res = loginUser(username, password, db_session)

                            # 3. Handle Result safely
                            if api_res and api_res.get("status"):
                                st.session_state.logged_in = True
                                st.rerun()
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
# def login_page_logic():
#     try:
#         st.markdown("""
#                     <style>
#                     /* This targets the main content area */
#                     .main .block-container {
#                         display: flex;
#                         flex-direction: column;
#                         justify-content: center; /* Vertical centering */
#                         height: 90vh; /* Takes up 90% of the viewport height */
#                     }
#
#                     /* Optional: Make the login box itself look larger/taller */
#                     [data-testid="stVerticalBlockBorderWrapper"] {
#                         padding: 50px !important;
#                         border-radius: 15px;
#                     }
#                     div.stButton > button {
#                         transition: all 0.3s ease-in-out; /* Smooth transition */
#                         border-radius: 8px;
#                     }
#
#                     /* 2. HOVER effect for the Login (Primary) button */
#                     /* Note: Streamlit 'Primary' buttons have a specific data-testid */
#                     div.stButton > button:hover {
#                         background-color: #ff4b4b; /* Change to your preferred hover color */
#                         color: white;
#                         border-color: #ff4b4b;
#                         transform: translateY(-2px); /* Slight lift effect */
#                         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#                     }
#
#                     /* 3. Specific style for the 'Login' button if you use type="primary" */
#                     button[kind="primary"]:hover {
#                         background-color: #2e7d32 !important; /* Darker green for login success feel */
#                         border-color: #2e7d32 !important;
#                     }
#                     </style>
#                 """, unsafe_allow_html=True)
#         # NOTE: below code is used for adding vertical spacing kind of customized space we are just creating column here we have created 3 column and we are using center one
#         left_co, cent_co, last_co = st.columns(spec=[2.9, 3.9, 0.6], vertical_alignment="center")
#         lef_bu, ce_bu, ri_bu = st.columns([3.1, 2, 2.2], vertical_alignment="center")
#         with cent_co:
#             with st.container():
#                 st.title("Login to System")
#                 username = st.text_input("Username", placeholder="Enter your username", width=300,
#                                          label_visibility="collapsed")
#                 password = st.text_input("Password", type="password", placeholder="Enter your password", width=300,
#                                          label_visibility="collapsed")
#
#                 cent_co_left, cent_co_mid, cent_co_right = st.columns([1, 2, 2], gap="xxsmall")
#                 with cent_co_left:
#                     if st.button("Login", icon_position="right", width=100):
#                         if not username or not password:
#                             st.warning("Please enter both credentials.")
#                         else:
#                             is_admin = (username == "admin" and password == "admin1")
#                             api_res = loginUser(username, password, db) if not is_admin else {"status": True}
#
#                         if api_res.get("status"):
#                             st.session_state.logged_in = True
#                             st.success("Logged in")
#                             st.rerun()
#                         else:
#                             st.error("*********** username or password",width="stretch")
#
#                 with cent_co_mid:
#                     if st.button("Change Password", icon_position="left", width="content"):
#                         change_password_dialog()
#                         if change_password_dialog:
#                             st.success("Change Password")
#
#     except Exception as e:
#         print(f'Error at function {login_page_logic.__name__} : {e}')