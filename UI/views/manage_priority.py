import streamlit as st

from Backend.src.services.curd import retrieve_drop_down_of_users, retrieve_drop_down_menu_for_user, \
    add_priority_data_to_user, retrieve_drop_down_menu_for_specific_user
from Backend.src.services.database import SessionLocal
from Backend.src.services.utils import on_user_change, mark_change, validate_priorities, show_unsaved_changes_modal, \
    reset_priorities, get_index

db = SessionLocal()

with SessionLocal() as db_session:
    user_priority_drop_down_list = retrieve_drop_down_menu_for_user(db)
    user_drop_down_dict = retrieve_drop_down_of_users(db)

print(f'testing result of user_priority_drop_down_list: {user_priority_drop_down_list}')

if "user" not in st.session_state and user_drop_down_dict:
    st.session_state.user = list(user_drop_down_dict.keys())[0]


def manage_page_logic():

    # ================= INIT =================
    keys_to_init = {
        "user": None,
        "selected_user": None,
        "submit_status": False,
        "form_change": False,
        "show_warning": False,
        "pending_user": None,
        "show_success_msg": False   #ADDED
    }

    for key, value in keys_to_init.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # ================= SUCCESS MESSAGE =================
    if st.session_state.show_success_msg:
        st.success("Priority updated successfully")
        st.session_state.show_success_msg = False

    # ================= RESET AFTER SUBMIT =================
    if st.session_state.submit_status:
        reset_priorities()
        st.session_state.submit_status = False

    with st.container():
        st.header("Manage Priority", text_alignment="center")

        user_list = list(user_drop_down_dict.keys())
        _, content_col, _ = st.columns([0.1, 4, 0.1])

        with content_col:

            # ================= USER SELECT =================
            with st.container(border=False, height=70, width=900):
                with st.container(border=True, height=70, width=900, horizontal_alignment='center'):
                    content_user, content_dropdown, _ = st.columns([0.5, 0.5, 0.1])

                    with content_user:
                        st.write("user")

                    with content_dropdown:
                        dropdown, _ = st.columns([1, 0.1])

                        with dropdown:
                            st.selectbox(
                                options=user_list,
                                index=user_list.index(
                                    st.session_state.selected_user or user_list[0]
                                ),
                                label="User",
                                label_visibility="collapsed",
                                key="user_temp",
                                on_change = reset_priorities,
                                kwargs={"to_fetch": True,}
                            )

                            selected_user = st.session_state.user_temp

                            if st.session_state.selected_user is None:
                                st.session_state.selected_user = user_list[0]

                            elif selected_user != st.session_state.selected_user:

                                if st.session_state.form_change:
                                    st.session_state.show_warning = True
                                    st.session_state.pending_user = selected_user
                                else:
                                    st.session_state.selected_user = selected_user

            # ================= PRIORITIES =================
            with st.container(border=True, height=280, width=900):
                if_priority_exists = retrieve_drop_down_menu_for_specific_user(db, selected_user)
                print(f' find out what if_priority_exists returns {if_priority_exists} ')
                if if_priority_exists:
                    # print(f'if Priority exists we are printing them : {if_priority_exists}')
                    p1, p2, p3 = if_priority_exists
                    print(f'p1 : {p1}, p2 : {p2}, p3 : {p3} ')
                    print(f'selected user is from manage priority {st.session_state.selected_user}')
                    with st.container(border=True, height=70, width=900):
                        c1, c2, _ = st.columns([0.5, 0.5, 0.1])
                        with c1:
                            st.write("Priority 1")
                        with c2:
                            st.selectbox(
                                options=user_priority_drop_down_list,
                                index=get_index(user_priority_drop_down_list, p1),
                                label="Priority1",
                                label_visibility="collapsed",
                                key="priority1",
                                on_change=mark_change
                            )

                    # Priority 2
                    with st.container(border=True, height=70, width=900):
                        c1, c2, _ = st.columns([0.5, 0.5, 0.1])
                        with c1:
                            st.write("Priority 2")
                        with c2:
                            st.selectbox(
                                options=user_priority_drop_down_list,
                                index=get_index(user_priority_drop_down_list, p2),
                                label="Priority2",
                                label_visibility="collapsed",
                                key="priority2",
                                on_change=mark_change
                            )

                    # Priority 3
                    with st.container(border=True, height=70, width=900):
                        c1, c2, _ = st.columns([0.5, 0.5, 0.1])
                        with c1:
                            st.write("Priority 3")
                        with c2:
                            st.selectbox(
                                options=user_priority_drop_down_list,
                                index=get_index(user_priority_drop_down_list, p3),
                                label="Priority3",
                                label_visibility="collapsed",
                                key="priority3",
                                on_change=mark_change
                            )
                else:
                    # Priority 1
                    with st.container(border=True, height=70, width=900):


                        c1, c2, _ = st.columns([0.5, 0.5, 0.1])
                        with c1:
                            st.write("Priority 1")
                        with c2:
                            st.selectbox(
                                options=user_priority_drop_down_list,
                                label="Priority1",
                                label_visibility="collapsed",
                                key="priority1",
                                on_change=mark_change
                            )

                    # Priority 2
                    with st.container(border=True, height=70, width=900):
                        c1, c2, _ = st.columns([0.5, 0.5, 0.1])
                        with c1:
                            st.write("Priority 2")
                        with c2:
                            st.selectbox(
                                options=user_priority_drop_down_list,
                                label="Priority2",
                                label_visibility="collapsed",
                                key="priority2",
                                on_change=mark_change
                            )

                    # Priority 3
                    with st.container(border=True, height=70, width=900):
                        c1, c2, _ = st.columns([0.5, 0.5, 0.1])
                        with c1:
                            st.write("Priority 3")
                        with c2:
                            st.selectbox(
                                options=user_priority_drop_down_list,
                                label="Priority3",
                                label_visibility="collapsed",
                                key="priority3",
                                on_change=mark_change
                            )

            # ================= SUBMIT =================
            with st.container(border=False, height=110, width=900):
                _, button_box, _ = st.columns([1, 1, 1])

                with button_box:
                    if st.button("Submit", use_container_width=True):

                        if not validate_priorities():
                            st.stop()

                        selected_name = st.session_state.selected_user
                        selected_id = user_drop_down_dict.get(selected_name)

                        st.session_state.admin_form_data = {
                            "user": st.session_state.user,
                            "priority_1": st.session_state.priority1,
                            "priority_2": st.session_state.priority2,
                            "priority_3": st.session_state.priority3,
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
                            st.session_state.show_success_msg = True   # ADDED

                            user_list = list(user_drop_down_dict.keys())
                            current_index = user_list.index(selected_name)

                            if current_index < len(user_list) - 1:
                                st.session_state.selected_user = user_list[current_index + 1]
                                st.session_state.form_change = False
                                st.rerun()
                            else:
                                st.success("You have reached the end of the list!")

    # ================= WARNING MODAL =================
    if st.session_state.show_warning:
        print(f'Selected user is {st.session_state.selected_user}')
        show_unsaved_changes_modal(db, user_drop_down_dict)

    return None