import inspect

import bcrypt
import streamlit as st
import inspect
from .curd import change_password, add_priority_data_to_user, retrieve_drop_down_menu_for_specific_user
from .database import SessionLocal

func_name = inspect.currentframe().f_code.co_name

@st.dialog("Change Your Password")
def change_password_dialog():
    st.write("Please verify your email and set a new password.")

    email_input = st.text_input("Confirm Email", placeholder="Enter your email")
    new_pw = st.text_input("New Password", type="password", placeholder="Enter new password")
    confirm_pw = st.text_input("Confirm New Password", type="password")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update", type="primary", use_container_width=True):
            if not email_input or not new_pw:
                st.error("All fields are required.")
            elif new_pw != confirm_pw:
                st.error("Passwords do not match!")
            else:
                # Use a new DB session for the update
                with SessionLocal() as db_session:
                    res = change_password(db_session, email_input, new_pw)

                if res.get("status"):
                    st.success("Password updated successfully!")
                    # Short pause so user can see success, then close
                    st.rerun()
                else:
                    st.error(res.get("message", "Update failed"))
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

def validate_password(password : bytes, hashed_password : bytes):
    try:
        #print(f'Db Password : {password}')
        #print(f'Entered and coinverted  Password : {hashed_password}')
        # NOTE: for now lets convert passowrd to bytes to match
        if bcrypt.checkpw(password, hashed_password):
            print("Password match!")
            return True
        else:
            print("Incorrect password.")
            return False
    except Exception as e:
        print(f"Error at {validate_password.__name__} error: {str(e)}")
        raise


def on_user_change():
    new_user = st.session_state.user

    if st.session_state.selected_user is None:
        st.session_state.selected_user = new_user
        return
    elif st.session_state.form_change:
        st.session_state.show_warning = True
        st.session_state.pending_user = new_user
        return

    else:
        st.session_state.selected_user = new_user


def mark_change():
    st.session_state.form_change = True


def validate_priorities():
    p1 = st.session_state.priority1
    p2 = st.session_state.priority2
    p3 = st.session_state.priority3

    values = [p1, p2, p3]

    if len(set(values)) != 3:
        st.error("Priority values must not be same")
        return False

    return True


def reset_priorities(to_fetch:bool=False):
    try:

        new_user = st.session_state.get("user_temp")
        if to_fetch:
            #print('inside if part of reset_priorities')
            with SessionLocal() as db_session:
                res = retrieve_drop_down_menu_for_specific_user(db_session, new_user)

                p1, p2, p3 = res if res else ("-", "-", "-")
                st.session_state.priority1 = p1
                st.session_state.priority2 = p2
                st.session_state.priority3 = p3

                st.session_state.selected_user = new_user
        else:
            st.session_state.priority1 = "-"
            st.session_state.priority2 = "-"
            st.session_state.priority3 = "-"
    except Exception as e :
        print(f'error at reset_priorities {e}')
        raise




@st.dialog("Unsaved Changes")
def show_unsaved_changes_modal(db,user_drop_down_dict):
    if st.session_state.show_warning:
            st.warning("You have unsaved changes!")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Save"):
                    if not validate_priorities():
                        st.stop()

                    selected_name = st.session_state.selected_user
                    selected_id = user_drop_down_dict.get(selected_name)
                    res = add_priority_data_to_user(
                        db,
                        selected_id,
                        selected_name,
                        st.session_state.priority1,
                        st.session_state.priority2,
                        st.session_state.priority3
                    )
                    if res:
                        st.session_state.submit_status = True
                        st.toast('You changes are saved.')

                    st.session_state.form_change = False
                    st.session_state.selected_user = st.session_state.pending_user
                    st.session_state.show_warning = False
                    st.rerun()

            with col2:
                if st.button("Discard"):
                    reset_priorities()
                    # Reset state
                    st.session_state.form_change = False
                    st.session_state.selected_user = st.session_state.pending_user
                    st.session_state.show_warning = False
                    st.toast('You changes are  discarded.')
                    st.rerun()
    return None

def get_index(user_priority_drop_down_list, val):
    return user_priority_drop_down_list.index(val)