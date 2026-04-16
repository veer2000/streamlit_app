import sys
import streamlit.components.v1 as components
import streamlit as st
import inspect
import os
from streamlit_quill import st_quill
from Backend.src.services.utils import view_email, clean_html_for_quill

# folder_path = r"C:\Users\raghuveer\PyCharmMiscProject\streamlit_ui\UI"  #Note: Or "MyReports" for a relative path
# file_name = "testfile.docx"
# full_path = os.path.join(folder_path, file_name)
# os.makedirs(folder_path, exist_ok=True)

func_name = inspect.currentframe().f_code.co_name


def enable_edit():
    st.session_state.editing = True

st.title("Home Page",text_alignment="center")
st.markdown("---")


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
            is_editing = st.session_state.get("editing", False)
            st.button(
                "Edit AI Response",
                use_container_width=True,
                disabled=is_editing,
                on_click=lambda: st.session_state.update({"editing": True})
            )

        with col2:
            st.button("Submit Response", use_container_width=True,
              on_click=lambda: st.session_state.update({"editing": False}))


    except Exception as e:
        st.error(f"Error in card2: {e}")


def homepage():
    try:
        card1_res = card1()
        card2(card1_res)
    except Exception as e:
        raise

# homepage()
