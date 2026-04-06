import inspect

import bcrypt
import streamlit as st
import re
import inspect

from .curd import change_password, add_priority_data_to_user
from .database import SessionLocal

func_name = inspect.currentframe().f_code.co_name

def view_email(email_data):
    try:
        """Card 1: Displays the incoming email details."""
        st.markdown("""
                    <style>
                    .email-body-container {
                        min-height: 100px;
                        max-height: 600px; /* Optional: adds a scrollbar only if it gets REALLY long */
                        overflow-y: auto;
                        padding: 15px;
                        border: 1px solid #f0f2f6;
                        border-radius: 10px;
                        background-color: #ffffff;
                    }
                    </style>
                """, unsafe_allow_html=True)
        with st.container(border=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**From:** `{email_data[0]['from']['emailAddress']['name']}`")
                st.markdown(f"**Subject:** {email_data[0]['subject']}")
            with col2:
                st.markdown(f"**Time:** `{email_data[0]['receivedDateTime'][:10]}`")  # Simplified date

            st.divider()

            st.markdown("**Body:**")

            html_content = email_data[0]["body"]["content"]

            clean_content = clean_html_for_quill(html_content)
            #
            st.markdown(
                f'<div class="email-body-container">{clean_content}</div>',
                unsafe_allow_html=True
            )

            return email_data
    except Exception as e:
        print(f'Error at {view_email.__name__} : {e}')
        raise

def email_interface():
    st.subheader("📧 Compose Email", divider="blue")

    # The main email card/container
    with st.container(border=True):
        # Header: Recipient and Subject
        to_address = st.text_input("To", placeholder="example@domain.com")
        subject = st.text_input("Subject", placeholder="Enter subject here...")

        st.divider()

        # Body: The main message area
        # height=300 mimics the large blank space in your image
        body = st.text_area("Message", height=300, label_visibility="collapsed",
                            placeholder="Write your message here...")

        st.divider()

        # Footer: Action buttons and icons
        col_send, col_icons = st.columns([1, 4])

        with col_send:
            if st.button("SEND", type="primary", use_container_width=True):
                st.success("Email Sent!")
                # Insert your sending logic here (e.g., smtplib)

        with col_icons:
            st.markdown("""
                <div style="display: flex; gap: 15px; font-size: 20px; padding-top: 5px; color: gray;">
                    <span>🔡</span> <span>😊</span> <span>📎</span> <span>🖼️</span> <span>🔗</span> <span>⭐</span> <span>🗑️</span>
                </div>
            """, unsafe_allow_html=True)


def clean_html_for_quill(raw_html):
    try:
        if not raw_html:
            return ""

        body_match = re.search(r'<body[^>]*>(.*?)</body>', raw_html, re.IGNORECASE | re.DOTALL)
        content = body_match.group(1) if body_match else raw_html

        content = re.sub(r'<(html|head|meta|style|title)[^>]*>.*?</\1>', '', content, flags=re.IGNORECASE | re.DOTALL)

        def transform_div_to_span(match):
            style = match.group(1)
            text = match.group(2)
            return f'<p><span style="{style}">{text}</span></p>'

        content = re.sub(r'<div[^>]*style="([^"]*)"[^>]*>(.*?)</div>', transform_div_to_span, content,
                         flags=re.IGNORECASE | re.DOTALL)

        content = re.sub(r'</?(html|head|body|div)[^>]*>', '', content, flags=re.IGNORECASE)

        content = content.replace('<p></p>', '').replace('<p><br></p>', '')

        return content.strip()
    except Exception as e:
        print(f' Error at {func_name} method :{clean_html_for_quill.__name__} error : {e}')
        raise


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
        print(f'Db Password : {password}')
        print(f'Entered and coinverted  Password : {hashed_password}')
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



def reset_priorities():
    st.session_state.priority1 = "-"
    st.session_state.priority2 = "-"
    st.session_state.priority3 = "-"




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
                    # reset_priorities()

                    st.session_state.form_change = False
                    st.session_state.selected_user = st.session_state.pending_user
                    st.session_state.show_warning = False
                    st.rerun()

            with col2:
                if st.button("Discard"):
                    # st.session_state.priority1 = "-"
                    # st.session_state.priority2 = "-"
                    # st.session_state.priority3 = "-"
                    reset_priorities()
                    # Reset state
                    st.session_state.form_change = False
                    st.session_state.selected_user = st.session_state.pending_user
                    st.session_state.show_warning = False
                    st.toast('You changes are  discarded.')
                    st.rerun()
    return None