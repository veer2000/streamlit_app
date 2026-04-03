import streamlit as st

from Backend.src.services.curd import retrieve_drop_down_menu, retrieve_drop_down_of_users
from Backend.src.services.database import SessionLocal
from Backend.src.services.utils import on_user_change, mark_change, validate_priorities

db = SessionLocal()

with SessionLocal() as db_session:
    priority_drop_down_list = retrieve_drop_down_menu(db)
    user_drop_down_list = retrieve_drop_down_of_users(db)
    print(f'user_drop_down_list value {user_drop_down_list}')


# ADD THIS BLOCK
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None

if "form_change" not in st.session_state:
    st.session_state.form_change = False

if "show_warning" not in st.session_state:
    st.session_state.show_warning = False

if "pending_user" not in st.session_state:
    st.session_state.pending_user = None


def admin_page_logic():
    with st.container():
        st.header("Admin Page", text_alignment="center")

        _, content_col, _ = st.columns([1,2.9,1])
        # user_dropdown_list = ["-","User 1", "User 2", "User 3"]
        # priority_drop_down_list = all_drop_down_values()
        with content_col:
            with st.container(border=False,height=70, width=900):
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'):
                    content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
                    with content_user:
                        st.write("user")
                    with content_dropdown:
                        dropdown, _ = st.columns([1,0.1])
                        with dropdown:
                            # st.selectbox(options=("-","User 1", "User 2", "User 3"), label="User",label_visibility="collapsed", key="user")
                            st.selectbox(options=user_drop_down_list, label="User",label_visibility="collapsed", key="user", on_change=on_user_change)
            with st.container(border=True, height=280, width=900):
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'): #border=True,
                    content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
                    with content_user:
                        st.write("Priority 1")
                    with content_dropdown:
                        dropdown, _ = st.columns([1,0.1])
                        with dropdown:
                            # st.selectbox(options=("-","Priority1 Value", "Home phone", "Mobile phone"), label="Priority1",label_visibility="collapsed",key="priority1")
                            st.selectbox(options=priority_drop_down_list, label="Priority1",label_visibility="collapsed",key="priority1", on_change=mark_change)
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'):
                    content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
                    with content_user:
                        st.write("Priority 2")
                    with content_dropdown:
                        dropdown, _ = st.columns([1,0.1])
                        with dropdown:
                            # st.selectbox(options=("-", "Priority2", "Home phone", "Mobile phone"), label="Priority2",label_visibility="collapsed", key="priority2")
                            st.selectbox(options=priority_drop_down_list, label="Priority2",label_visibility="collapsed", key="priority2", on_change=mark_change)
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'):
                    content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
                    with content_user:
                        st.write("Priority 3")
                    with content_dropdown:
                        dropdown, _ = st.columns([1,0.1])
                        with dropdown:
                            # st.selectbox(options=("-", "Priority3", "Home phone", "Mobile phone"), label="Priority3",label_visibility="collapsed", key="priority3")
                            st.selectbox(options=priority_drop_down_list, label="Priority3",label_visibility="collapsed", key="priority3", on_change=mark_change)
            with st.container(border=False, height=110, width=900):
                _, button_box,_ = st.columns([1,1,1])
                with button_box:
                    if st.button("Submit", use_container_width=True):
                        if not validate_priorities():
                            st.stop()
                        st.session_state.admin_form_data = {
                            "user": st.session_state.user,
                            "priority_1": st.session_state.priority1,
                            "priority_2": st.session_state.priority2,
                            "priority_3": st.session_state.priority3,
                            # "priority_4": st.session_state.priority4,
                        }
                        st.session_state.form_change = False
                        # NOTE: we are printing value using tost
                        st.toast(st.session_state.admin_form_data)


    if st.session_state.show_warning:
        with st.modal("Unsaved Changes"):
            st.warning("You have unsaved changes!")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Save"):
                    st.session_state.form_change = False
                    st.session_state.selected_user = st.session_state.pending_user
                    st.session_state.user = st.session_state.pending_user
                    st.session_state.show_warning = False

            with col2:
                if st.button("Discard"):
                    st.session_state.form_change = False
                    st.session_state.selected_user = st.session_state.pending_user
                    st.session_state.user = st.session_state.pending_user
                    st.session_state.show_warning = False

    return None
admin_page_logic()


# with st.container(border=True, height=90, width=900, horizontal_alignment='center'):
#                 content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
#                 with content_user:
#                     st.write("Priority 4")
#                 with content_dropdown:
#                     dropdown, _ = st.columns([1,0.1])
#                     with dropdown:
#                         st.selectbox(options=("-", "Priority4", "Home phone", "Mobile phone"), label="Priority4",label_visibility="collapsed", key="priority4")