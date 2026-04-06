import sys
import streamlit.components.v1 as components
import streamlit as st
import inspect
import os
from streamlit_quill import st_quill

from Backend.src.services.curd import submit_response
# from Backend.src.services.utils import view_email, clean_html_for_quill
from Backend.src.services.test_utils import view_email, clean_html_for_quill
# from ..integrated_Agent_for_emailDraft import get_draft_email
# from Backend.src.services.integrated_Agent_for_emailDraft import get_draft_email
# from Backend.src.services.integrated_Agent_for_emailDraft import get_draft_email
# from Backend.src.services.submit_response import submit_response
# from Backend.src.services.access_emails import submit_response

# folder_path = r"C:\Users\raghuveer\PyCharmMiscProject\streamlit_ui\UI"  #Note: Or "MyReports" for a relative path
# file_name = "testfile.docx"
# full_path = os.path.join(folder_path, file_name)
# os.makedirs(folder_path, exist_ok=True)

func_name = inspect.currentframe().f_code.co_name


# if "msg_id" not in st.session_state:
#     st.session_state.msg_id = 0


def enable_edit():
    st.session_state.editing = True


st.title("Home Page")  # ,text_alignment="center"
st.markdown("---")

emaildata_template = [
    {
        "@odata.etag": "W/\"CQAAABYAAA***********************vYHo\"",
        "id": "AAMk*************************************************************MAAAjLzc**************************************1oAAA=",
        "receivedDateTime": "2026-03-26T06:45:08Z",
        "subject": "Attached PDF",
        "body": {
            "contentType": "html",
            "content": "<html><head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"><style type=\"text/css\" style=\"display:none\">\r\n<!--\r\np\r\n\t{margin-top:0;\r\n\tmargin-bottom:0}\r\n-->\r\n</style></head><body dir=\"ltr\"><div class=\"elementToProof\" style=\"font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0); background-color: yellow; display: inline-block; padding: 2px;\">Do smokers lungs heal after quitting?I’ve smoked for 40 years now but was never a “heavy” smoker. Something like a pack every two or three days kind of a smoker… I recently quit cold turkey, it’s been 40 days or so now. I bummed a stick or two from friends when I got together with them at my local 3 cushion billiards sport hall in the first two weeks. So in order to be able to keep quitting smoking I quit my 3 cushion billiard playing habit also. What else? When I quit I bought some meats and foods I thought I would crave (I am alone nowadays as the family is over at the summer cottage) but I couldn’t eat them. All I eat practically is yogurt and cinnamon, and occasionally I melt some cheddar and eat that. Otherwise I have lost all appetite for deliciousness, as it were. I don’t want to eat the stuff I bought since I think “what’s the use of eating them when I can’t light up afterwards?”</div><div class=\"elementToProof\" style=\"font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)\"><br></div><div class=\"elementToProof\" style=\"font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)\"><br></div></body></html>"
        },
        "from": {
            "emailAddress": {
                "name": "test guy",
                "address": "test@mail.com"
            }
        }
    }
]

# In 01_HomePage.py

# 1. Add the import for fetching the email at the top
# from Backend.src.services.access_emails import get_allocated_email



def card1():
    try:
        # Fetch email ONLY if it's not already in the session state
        # if "current_email" not in st.session_state:
        #     st.session_state.current_email = get_allocated_email()
        if "current_email" not in st.session_state:
            st.session_state.current_email = emaildata_template
            st.session_state.drafted_text = st.session_state.current_email[0]['body']['content']
        if 'drafted_text' not in st.session_state:
            st.session_state.drafted_text = st.session_state.current_email
        # Pass the stored email to the view function
        email = view_email(st.session_state.current_email)
        msg_id = email[0]['id']
        st.session_state["msg_id"] = msg_id
        return email
    except Exception as e:
        print(f'Error at {func_name}: {card1.__name__} : {e}')
        raise


# Callback function to handle the submit action cleanly
def handle_submit():
    # Submit the response
    # submit_response(st.session_state["msg_id"], st.session_state.drafted_text)
    submit_response(st.session_state["msg_id"])

    # Clear the session state so the NEXT rerun fetches a new email and new draft
    st.session_state.editing = False
    if "current_email" in st.session_state:
        del st.session_state["current_email"]
    if "drafted_text" in st.session_state:
        del st.session_state["drafted_text"]


def card2(emailcontent):
    try:
        st.subheader("Draft Response")

        # Fetch AI Draft ONLY if we haven't drafted one for this email yet
        # if "drafted_text" not in st.session_state:
        #     st.session_state.drafted_text = get_draft_email(emailcontent)

        if "editing" not in st.session_state:
            st.session_state.editing = False

        # =========================
        # VIEW MODE
        # =========================
        if not st.session_state.editing:
            with st.container(border=True):
                st.markdown(
                    st.session_state.drafted_text,
                    unsafe_allow_html=True
                )
        # =========================
        # EDIT MODE
        # =========================
        else:
            st.write("🟡 EDIT MODE")
            try:
                buffer_text = st_quill(
                    value=st.session_state.drafted_text,
                    html=True,
                    toolbar=[
                        ["bold", "italic", "underline"],
                        [{"color": []}, {"background": []}]
                    ],
                    key="quill_editor"
                )
            except Exception:
                buffer_text = st.text_area(
                    "Edit Content",
                    value=st.session_state.drafted_text,
                    height=300
                )

            if buffer_text is not None:
                st.session_state.drafted_text = buffer_text

        # =========================
        # ACTION BUTTONS
        # =========================
        st.markdown("---")
        _, col1, col2, _ = st.columns([1, 1, 1, 1])

        with col1:
            is_editing = st.session_state.get("editing", False)
            st.button(
                "Edit AI Response",
                use_container_width=True,
                disabled=is_editing,
                on_click=lambda: st.session_state.update({"editing": True})
            )

        with col2:
            # Use the dedicated callback function here
            st.button(
                "Submit Response",
                use_container_width=True,
                on_click=handle_submit
            )

    except Exception as e:
        st.error(f"Error in card2: {e}")
        raise


def homepage():
    try:
        card1()
        # email_res = card1()
        # print(f' from homepage {card1_res}')
        # NOTE: this callis to show card2 which has quill to edit content
        # card2(email_res, llm_response)
        # card2(email_res)
    except Exception as e:
        raise


homepage()













