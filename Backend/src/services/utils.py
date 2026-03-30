import inspect

import bcrypt
import streamlit as st
import re
import inspect

from .curd import change_password
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
            st.write('hi 3')
            # Using markdown with emojis to simulate the toolbar icons in your image
            # st.markdown("""
            #     <div style="display: flex; gap: 15px; font-size: 20px; padding-top: 5px; color: gray;">
            #         <span>🔡</span> <span>😊</span> <span>📎</span> <span>🖼️</span> <span>🔗</span> <span>⭐</span> <span>🗑️</span>
            #     </div>
            # """, unsafe_allow_html=True)


def clean_html_for_quill(raw_html):
    try:
        if not raw_html:
            return ""

            # 1. Extract the content inside <body>
        body_match = re.search(r'<body[^>]*>(.*?)</body>', raw_html, re.IGNORECASE | re.DOTALL)
        content = body_match.group(1) if body_match else raw_html

        # 2. Strip out all the <head>, <style>, <meta> stuff
        content = re.sub(r'<(html|head|meta|style|title)[^>]*>.*?</\1>', '', content, flags=re.IGNORECASE | re.DOTALL)

        # 3. TRANSFORM DIVS TO SPANS (The "Quill Fix")
        # This regex finds <div style="...">...</div> and captures the style and the inner text.
        # It then converts it to <p><span style="...">...</span></p>
        def transform_div_to_span(match):
            style = match.group(1)
            text = match.group(2)
            # We wrap it in <p> because Quill requires every line to be in a block-level tag
            return f'<p><span style="{style}">{text}</span></p>'

        content = re.sub(r'<div[^>]*style="([^"]*)"[^>]*>(.*?)</div>', transform_div_to_span, content,
                         flags=re.IGNORECASE | re.DOTALL)

        # 4. Final Cleanup: Remove remaining structural tags but keep the content
        content = re.sub(r'</?(html|head|body|div)[^>]*>', '', content, flags=re.IGNORECASE)

        # 5. Fix double-spacing that sometimes occurs during regex conversion
        content = content.replace('<p></p>', '').replace('<p><br></p>', '')

        return content.strip()
    except Exception as e:
        print(f' Error at {func_name} method :{clean_html_for_quill.__name__} error : {e}')
        raise


@st.dialog("Change Your Password")
def change_password_dialog():
    st.write("Please verify your email and set a new password.")

    # Input fields inside the modal
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

# def generate_hash_pass(password):
#     try:
#         print(f'Enterted method {generate_hash_pass.__name__}')
#         password_bytes = password.encode('utf-8')
#         hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
#         print(f'Hashed Password: {hashed_password}')
#         # return hashed_password.decode('utf-8')
#         return hashed_password
#     except Exception as e:
#         print(f"Error at {generate_hash_pass.__name__}error: {str(e)}")
#         raise


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

"""
"value": [
    {
      "@odata.etag": "W/\"CQAAABYAAAAjLzc+n7YHS4d9ZMHcizm9AAKfvYHo\"",
      "id": "AAMkAGRhN2M4ZjIyLTQ0ZmQtNGNiMi1hZDM4LTJmZGY3NjkwNmY3ZgBGAAAAAABadgoXVbP3R4yyxv4r5CRqBwAjLzc_n7YHS4d9ZMHcizm9AAAAAAEMAAAjLzc_n7YHS4d9ZMHcizm9AAEvpo1oAAA=",
      "receivedDateTime": "2026-03-26T06:45:08Z",
      "hasAttachments": true,
      "subject": "Attached PDF",
      "body": {
        "contentType": "text",
        "content": "Please check attached pdf\r\n\r\n\r\n"
      },
      "from": {
        "emailAddress": {
          "name": "Abhishek Gambhire",
          "address": "AbhishekG@koolatron.com"
        },
        "to": {
            "emailAddress": {
            "name": "Sham",
            "address": "Sham@Koolatron.com"
        }
    }
  ]
"""