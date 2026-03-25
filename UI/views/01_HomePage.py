import sys

import streamlit as st
import inspect
import os

from Backend.src.services.curd import get_allocated_email, get_draft_response

func_name = inspect.currentframe().f_code.co_name
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

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
                new_text = st.text_area("Edit your Draft", st.session_state.drafted_text, height=300)
                st.session_state.drafted_text = new_text
            else:
                st.markdown(f"<h5 style='text-align: center;'>{st.session_state.drafted_text}</h3>", unsafe_allow_html=True)

            # # 1. Center the Header
            # res = get_draft_response(emailContent)
            # #NOTE: here we are using .markdown to add custom CSS to adjust as per our need
            # st.markdown(f"<h3 style='text-align: center;'>{res}</h1>", unsafe_allow_html=True)

            _, col1, col2, col3, _ = st.columns([1, 1, 1, 1, 1])

            with col1:
                if st.button("Edit", use_container_width=True):
                    st.session_state.editing = True
                    st.rerun()
            with col2:
                if st.button("Save", use_container_width=True):
                    st.session_state.editing = False
                    # NOTE: we will store drafted version in database using version number
                    st.success("Your Draft has been saved")
                    st.rerun()
            with col3:
                if st.button("Submit", use_container_width=True):
                    #NOTE: we will make a api call for email or we store data in database
                    st.info("success")
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