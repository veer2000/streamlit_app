import sys
import streamlit.components.v1 as components
from htmldocx import HtmlToDocx
from docx import Document
import streamlit as st
import inspect
import os
from streamlit_quill import st_quill
from Backend.src.services.curd import get_allocated_email, get_draft_response, submit_response

folder_path = r"C:\Users\raghuveer\PyCharmMiscProject\streamlit_ui\UI"  # Or "MyReports" for a relative path
file_name = "testfile.docx"
full_path = os.path.join(folder_path, file_name)
os.makedirs(folder_path, exist_ok=True)

func_name = inspect.currentframe().f_code.co_name


st.title("Home Page",text_alignment="center")
st.markdown("---")
#
# st.header("Analyze and Visualize Data")
# st.write("This page will eventually display data fetched from your Backend API.")


def card1():
    try:
        st.subheader(" Email To Respond", text_alignment="center")

        # Using columns inside a card to show metrics
        with st.container(border=True):
            #st.header("Email Details", text_alignment="center")
            res = get_allocated_email()
            st.write(res)
            # col1, col2, col3 = st.columns(3, vertical_alignment="center",border=True)
            # col1.metric("Total Items", "1,240", "+5%")
            # col2.metric("Active Listings", "850", "-2%")
            # col3.metric("Out of Stock", "12", "Low")
        return res
    except Exception as e:
        print(f'Error at {func_name}: {card1.__name__} : {e}')
        raise

def card2(emailContent):
    try:
        st.subheader("Draft Response", anchor=False, text_alignment='center')  # anchor=False removes the hover link icon
        if "drafted_text" not in st.session_state:
            st.session_state.drafted_text = get_draft_response(emailContent)
        if "editing" not in st.session_state:
            st.session_state.editing = False

        with st.container(border=True):

            if st.session_state.editing:
                new_text = st_quill(
                    value=st.session_state.drafted_text,
                    html=True,
                    toolbar=["bold", "italic", "underline"], #, {"color": []}, {"background": []}
                    key="quill_editor"
                )

                st.session_state.drafted_text = new_text
            else:
                # st.markdown(f"<h5 style='text-align: center;'>{st.session_state.drafted_text}</h3>", unsafe_allow_html=True)
                st.markdown(st.session_state.drafted_text, unsafe_allow_html=True)

            # # 1. Center the Header
            # res = get_draft_response(emailContent)
            # #NOTE: here we are using .markdown to add custom CSS to adjust as per our need
            # st.markdown(f"<h3 style='text-align: center;'>{res}</h1>", unsafe_allow_html=True)
        with st.container():
            _, col1, col2, col3, _ = st.columns([1, 1, 1, 1, 1])

            with col1:
                if st.button("Edit", use_container_width=True):
                    st.session_state.editing = True
                    st.rerun()
            with col2:
                if st.button("Save", use_container_width=True):
                    st.session_state.editing = False
                    # NOTE: we will store drafted version in database using version number
                    # st.success("Your Draft has been saved",width="stretch")
                    document = Document()
                    new_parser = HtmlToDocx()
                    html_content = st.session_state.get("drafted_text") or ""
                    new_parser.add_html_to_document(html_content, document)
                    document.save(full_path)
                    # with open(full_path, "w", encoding="utf-8") as file:
                    #     file.write(st.session_state.drafted_text)
                    st.rerun()
            with col3:
                if st.button("Submit Response", use_container_width=True):
                    email_response = "sent successfully"
                    #NOTE: we will make a api call for email or we store data in database
                    res = submit_response(email_response)
                    st.toast("Email sent successfully!", icon="✅")

    except Exception as e:
        print(f'Error at {func_name}: {card2.__name__} : {e}')
        raise


def homepage():
    try:
        card1_res = card1()
        card2(card1_res)
    except Exception as e:
        raise

homepage()

# NOTE: below content is for colour change of the sdit section which we will place directly above new_text = st_quill(
# new_text = st.text_area("Edit your Draft", st.session_state.drafted_text, height=300)
# st.session_state.drafted_text = new_text
# components.html("""
#     <script>
#     const forceDarkQuill = () => {
#         // Find all iframes that might be the Quill editor
#         const iframes = window.parent.document.querySelectorAll('iframe');
#         iframes.forEach(iframe => {
#             try {
#                 const doc = iframe.contentDocument || iframe.contentWindow.document;
#                 // Change the background and text colors inside the iframe
#                 const editor = doc.querySelector('.ql-editor');
#                 const toolbar = doc.querySelector('.ql-toolbar');
#                 const container = doc.querySelector('.ql-container');
#
#                 if (editor) {
#                     editor.style.backgroundColor = "#0E1117";
#                     editor.style.color = "#FAFAFA";
#                 }
#                 if (toolbar) {
#                     toolbar.style.backgroundColor = "#262730";
#                     toolbar.style.borderColor = "#464b5d";
#                     // Make icons white
#                     toolbar.querySelectorAll('.ql-stroke').forEach(s => s.style.stroke = "#FAFAFA");
#                     toolbar.querySelectorAll('.ql-fill').forEach(f => f.style.fill = "#FAFAFA");
#                 }
#                 if (container) {
#                     container.style.backgroundColor = "#0E1117";
#                     container.style.borderColor = "#464b5d";
#                 }
#             } catch (e) { /* Ignore cross-origin errors if any */ }
#         });
#     };
#     // Run it once and then every second to ensure it stays dark
#     forceDarkQuill();
#     setInterval(forceDarkQuill, 1000);
#     </script>
# """, height=0)