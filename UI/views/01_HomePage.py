import sys
import streamlit.components.v1 as components
from htmldocx import HtmlToDocx
from docx import Document
import streamlit as st
import inspect
import os
from streamlit_quill import st_quill
from Backend.src.services.curd import get_allocated_email, get_draft_response, submit_response
from Backend.src.services.utils import email_interface, view_email, clean_html_for_quill

folder_path = r"C:\Users\raghuveer\PyCharmMiscProject\streamlit_ui\UI"  # Or "MyReports" for a relative path
file_name = "testfile.docx"
full_path = os.path.join(folder_path, file_name)
os.makedirs(folder_path, exist_ok=True)

func_name = inspect.currentframe().f_code.co_name

# st_quill("<p>INLINE TEST</p>", key="inline_test")

def enable_edit():
    st.session_state.editing = True

st.title("Home Page",text_alignment="center")
st.markdown("---")
#
# st.header("Analyze and Visualize Data")
# st.write("This page will eventually display data fetched from your Backend API.")
emaildata = [
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


def card1():
    try:
        return view_email(emaildata)
    except Exception as e:
        print(f'Error at {func_name}: {card1.__name__} : {e}')
        raise



def card2(emailcontent):
    try:
        st.subheader("Draft Response")

        # ✅ Extract content
        if isinstance(emailcontent, list) and len(emailcontent) > 0:
            raw_html = emailcontent[0].get("body", {}).get("content", "")
        else:
            st.error("Invalid email content")
            return

        cleaned_html = clean_html_for_quill(raw_html)

        # ✅ Initialize state
        if "editing" not in st.session_state:
            st.session_state.editing = False

        if "drafted_text" not in st.session_state:
            st.session_state.drafted_text = cleaned_html

        # =========================
        # ✅ VIEW MODE
        # =========================
        if not st.session_state.editing:
            with st.container(border=True):
                st.markdown(
                    st.session_state.drafted_text,
                    unsafe_allow_html=True
                )

        # =========================
        # ✅ EDIT MODE (LIVE EDIT)
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

            # 🔥 KEY CHANGE: auto-sync
            if buffer_text is not None:
                st.session_state.drafted_text = buffer_text

        # =========================
        # ✅ ACTION BUTTONS
        # =========================
        st.markdown("---")

        _, col1, col2, _ = st.columns([1, 1, 1, 1])

        with col1:
            if st.session_state.editing:
                if st.button("Save", use_container_width=True, key="save_btn"):
                    st.session_state.editing = False
                    st.rerun()
            else:
                if st.button("Edit AI Response", use_container_width=True, key="edit_btn"):
                    st.session_state.editing = True
                    st.rerun()

        with col2:
            if st.button("Submit Response", use_container_width=True):
                submit_response(st.session_state.drafted_text)
                st.toast("Email sent successfully!", icon="✅")

    except Exception as e:
        st.error(f"Error in card2: {e}")


# def card2(emailcontent):
#     try:
#         st.subheader("Draft Response", anchor=False)
#
#         if "editing" not in st.session_state:
#             st.session_state.editing = False
#
#         if "drafted_text" not in st.session_state:
#             email_body_data = emailcontent[0]["body"]["content"]
#             st.session_state.drafted_text = clean_html_for_quill(email_body_data)
#
#         st.write("DEBUG editing state:", st.session_state.get("editing"))
#
#         with st.container():
#             if st.session_state.editing:
#                 st.write("EDITOR MODE ACTIVE")
#
#                 buffer_text = st_quill(
#                     value=st.session_state.drafted_text,
#                     html=True,
#                     toolbar=["bold", "italic", "underline", {"color": []}, {"background": []}],
#                     key="quill_editor"
#                 )
#
#                 if st.button("Save Changes", type="primary", use_container_width=True):
#                     if buffer_text and buffer_text != "<p><br></p>":
#                         st.session_state.drafted_text = buffer_text
#
#                     st.session_state.editing = False
#                     st.rerun()
#
#                 if st.button("Cancel", use_container_width=True):
#                     st.session_state.editing = False
#                     st.rerun()
#
#             else:
#                 st.markdown(st.session_state.drafted_text, unsafe_allow_html=True)
#
#         _, col1, col2, _ = st.columns([1, 1, 1, 1])
#
#         with col1:
#             if not st.session_state.editing:
#                 st.button(
#                     "Edit AI Response",
#                     use_container_width=True,
#                     on_click=lambda: st.session_state.update({"editing": True})
#                 )
#
#         with col2:
#             if st.button("Submit Response", use_container_width=True):
#                 submit_response(st.session_state.drafted_text)
#                 st.toast("Email sent successfully!", icon="✅")
#
#     except Exception as e:
#         st.error(f"Error in card2: {e}")
# def card2(emailcontent):
#     try:
#         st.subheader("Draft Response", anchor=False, text_alignment='center')  # anchor=False removes the hover link icon
#         if "drafted_text" not in st.session_state:
#             email_body_data = emailcontent[0]["body"]["content"]
#             st.session_state.drafted_text = get_draft_response(email_body_data)
#             print(f'Draft Response from Card 2: {st.session_state.drafted_text}')
#             # print(f'Draft Response: {st.session_state.drafted_text}')
#             # st.session_state.drafted_text = "As digital sovereignty becomes a strategic requirement, organizations are rethinking how they deploy critical infrastructure and AI capabilities under tighter regulatory expectations and higher risk conditions. Microsoft’s approach to sovereignty is grounded in enabling enterprises, public sectors and regulated industries to participate in the digital economy securely, independently and on their own terms. The Microsoft Sovereign Cloud brings together productivity, security and cloud workloads to span both public and private environments. Customers can choose the right control posture for each workload, through a continuum of sovereign options protecting against fragmenting their architecture or increasing operational risk. Trust is built on confidence: confidence that data stays protected, controls are enforceable and operations can continue under real-world conditions"
#         if "editing" not in st.session_state:
#             st.session_state.editing = False
#
#         with st.container(border=True):
#
#             if st.session_state.editing:
#                 buffer_text = st_quill(
#                     value=st.session_state.drafted_text,
#                     html=True,
#                     toolbar=["bold", "italic", "underline", {"color": []}, {"background": []}],
#                     key="quill_editor"
#                 )
#
#                 st.session_state.drafted_text = buffer_text
#                 if st.button("Save Changes", type="primary", use_container_width=True):
#                     if buffer_text and buffer_text != "<p><br></p>":
#                         st.session_state.drafted_text = buffer_text
#                     st.session_state.editing = False
#                     st.rerun()
#                 if st.button("Cancel", use_container_width=True):
#                     st.session_state.editing = False
#                     st.rerun()
#             else:
#                 # st.markdown(f"<h5 style='text-align: center;'>{st.session_state.drafted_text}</h3>", unsafe_allow_html=True)
#                 display_html = st.session_state.drafted_text or "No content drafted yet."
#                 st.markdown(display_html, unsafe_allow_html=True)
#
#             # # 1. Center the Header
#             # res = get_draft_response(emailcontent)
#             # #NOTE: here we are using .markdown to add custom CSS to adjust as per our need
#             # st.markdown(f"<h3 style='text-align: center;'>{res}</h1>", unsafe_allow_html=True)
#         with st.container():
#             # _, col1, col2, col3, _ = st.columns([1, 1, 1, 1, 1])
#             _, col1, col2, _ = st.columns([1, 1, 1, 1])
#
#             with col1:
#                 if not st.session_state.editing:
#                     if st.button("Edit AI Response", use_container_width=True):
#                         st.session_state.editing = True
#                         st.rerun()
#             # with col2:
#             #     if st.button("Save", use_container_width=True):
#             #         st.session_state.editing = False
#             #         # NOTE: we will store drafted version in database using version number
#             #         # st.success("Your Draft has been saved",width="stretch")
#             #         document = Document()
#             #         new_parser = HtmlToDocx()
#             #         html_content = st.session_state.get("drafted_text") or ""
#             #         new_parser.add_html_to_document(html_content, document)
#             #         document.save(full_path)
#             #         # with open(full_path, "w", encoding="utf-8") as file:
#             #         #     file.write(st.session_state.drafted_text)
#             #         st.rerun()
#             with col2:
#                 if st.button("Submit Response", use_container_width=True):
#                     # Submit the HTML content stored in session state
#                     submit_response(st.session_state.drafted_text)
#                     st.toast("Email sent successfully!", icon="✅")
#
#     except Exception as e:
#         print(f'Error at {func_name}: {card2.__name__} : {e}')
#         raise


def homepage():
    try:
        card1_res = card1()
        card2(card1_res)
    except Exception as e:
        raise

homepage()

# [
#     {
#         "@odata.etag": "W/\"CQAAABYA***********************\"",
#         "id": "A************************************************************************************************************************oAAA=",
#         "receivedDateTime": "2026-03-26T06:45:08Z",
#         "subject": "Attached PDF",
#         "body": {
#             "contentType": "html",
#             "content": "<html><head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"><style type=\"text/css\" style=\"display:none\">\r\n<!--\r\np\r\n\t{margin-top:0;\r\n\tmargin-bottom:0}\r\n-->\r\n</style></head><body dir=\"ltr\"><div class=\"elementToProof\" style=\"font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)\">Please check attached pdf</div><div class=\"elementToProof\" style=\"font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)\"><br></div><div class=\"elementToProof\" style=\"font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)\"><br></div></body></html>"
#         },
#         "from": {
#             "emailAddress": {
#                 "name": "test",
#                 "address": "test@mail.com"
#             }
#         }
#     }
# ]

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