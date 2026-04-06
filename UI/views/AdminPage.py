import streamlit as st

from Backend.src.services.curd import retrieve_drop_down_menu, retrieve_drop_down_of_users, retrieve_drop_down_menu_for_user, \
    add_priority_data_to_user
from Backend.src.services.database import SessionLocal
from Backend.src.services.utils import on_user_change, mark_change, validate_priorities, show_unsaved_changes_modal, \
    reset_priorities

db = SessionLocal()

with SessionLocal() as db_session:
    priority_drop_down_list = retrieve_drop_down_menu(db)
    user_priority_drop_down_list = retrieve_drop_down_menu_for_user(db)
    user_drop_down_dict = retrieve_drop_down_of_users(db)
print(f'testing result of priority_drop_down_list : {priority_drop_down_list}')
print(f'testing result of user_priority_drop_down_list: {user_priority_drop_down_list}')
if "user" not in st.session_state and user_drop_down_dict:
    # Safely pick the first key from your database dictionary
    st.session_state.user = list(user_drop_down_dict.keys())[0]

if "submit_status" not in st.session_state:
    st.session_state.submit_status = False

if "selected_user" not in st.session_state:
    st.session_state.selected_user = None

if "form_change" not in st.session_state:
    st.session_state.form_change = False

if "show_warning" not in st.session_state:
    st.session_state.show_warning = False

if "pending_user" not in st.session_state:
    st.session_state.pending_user = None


if st.session_state.submit_status:
    reset_priorities()
    st.toast('submited you response')

def admin_page_logic():
    with st.container():
        st.header("Admin Page", text_alignment="center")
        user_list = list(user_drop_down_dict.keys())
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
                            st.selectbox(
                                options=user_list,
                                index=user_list.index(
                                    st.session_state.selected_user or user_list[0]
                                ),
                                label="User",
                                label_visibility="collapsed",
                                key="user_temp"
                            )
                            selected_user = st.session_state.user_temp

                            if st.session_state.selected_user is None:
                                st.session_state.selected_user = user_list[0]

                            elif selected_user != st.session_state.selected_user:

                                if st.session_state.form_change:
                                    st.session_state.show_warning = True
                                    st.session_state.pending_user = selected_user

                                    # st.session_state.user_temp = st.session_state.selected_user

                                else:
                                    st.session_state.selected_user = selected_user
            with st.container(border=True, height=280, width=900):
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'): #border=True,
                    content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
                    with content_user:
                        st.write("Priority 1")
                    with content_dropdown:
                        dropdown, _ = st.columns([1,0.1])
                        with dropdown:
                            # st.selectbox(options=priority_drop_down_list, label="Priority1",label_visibility="collapsed",key="priority1", on_change=mark_change)
                            st.selectbox(options=user_priority_drop_down_list, label="Priority1",label_visibility="collapsed",key="priority1", on_change=mark_change)
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'):
                    content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
                    with content_user:
                        st.write("Priority 2")
                    with content_dropdown:
                        dropdown, _ = st.columns([1,0.1])
                        with dropdown:
                            # st.selectbox(options=priority_drop_down_list, label="Priority2",label_visibility="collapsed", key="priority2", on_change=mark_change)
                            st.selectbox(options=user_priority_drop_down_list, label="Priority2",label_visibility="collapsed", key="priority2", on_change=mark_change)
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'):
                    content_user, content_dropdown, _ = st.columns([0.5,0.5,0.1])
                    with content_user:
                        st.write("Priority 3")
                    with content_dropdown:
                        dropdown, _ = st.columns([1,0.1])
                        with dropdown:
                            # st.selectbox(options=priority_drop_down_list, label="Priority3",label_visibility="collapsed", key="priority3", on_change=mark_change)
                            st.selectbox(options=user_priority_drop_down_list, label="Priority3",label_visibility="collapsed", key="priority3", on_change=mark_change)
            with st.container(border=False, height=110, width=900):
                _, button_box,_ = st.columns([1,1,1])
                with button_box:
                    if st.button("Submit", use_container_width=True):
                        if not validate_priorities():
                            st.stop()
                        selected_name = st.session_state.selected_user
                        selected_id = user_drop_down_dict.get(selected_name)
                        st.session_state.admin_form_data = {
                            # "user_id": selected_id,
                            "user": st.session_state.user,
                            "priority_1": st.session_state.priority1,
                            "priority_2": st.session_state.priority2,
                            "priority_3": st.session_state.priority3,
                            # "priority_4": st.session_state.priority4,
                        }
                        st.session_state.form_change = False
                        if add_priority_data_to_user(
                                db,
                                selected_id,
                                selected_name,
                                st.session_state.priority1,
                                st.session_state.priority2,
                                st.session_state.priority3
                        ):
                            st.session_state.submit_status = True

                            user_list = list(user_drop_down_dict.keys())
                            current_index = user_list.index(selected_name)

                            if current_index < len(user_list) - 1:
                                st.session_state.selected_user = user_list[current_index + 1]
                                st.session_state.form_change = False
                                # st.rerun()
                            else:
                                st.success("You have reached the end of the list!")


    if st.session_state.show_warning:
        print(f'Selected user is {st.session_state.selected_user}')
        show_unsaved_changes_modal(db,user_drop_down_dict)

    return None

#Note: this ios function call for execution do not comment or remove it or change its indent
admin_page_logic()