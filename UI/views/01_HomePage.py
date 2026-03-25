import sys

import streamlit as st
import inspect
import os

from Backend.src.services.curd import get_allocated_email, get_drafed_response

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
    except Exception as e:
        print(f'Error at {func_name}: {card1.__name__} : {e}')
        raise

def card2():
    try:
        st.subheader("Draft Response", anchor=False, text_alignment='center')  # anchor=False removes the hover link icon
        with st.container(border=True):
            # 1. Center the Header
            res = get_drafed_response()
            #NOTE: here we are using .markdown to add custom CSS to adjust as per our need
            st.markdown(f"<h1 style='text-align: center;'>{res}</h1>", unsafe_allow_html=True)

            _, col1, col2, col3, _ = st.columns([1, 1, 1, 1, 1])

            with col1:
                st.button("Edit", use_container_width=True)
            with col2:
                st.button("Save", use_container_width=True)
            with col3:
                st.button("Submit", use_container_width=True)
    except Exception as e:
        print(f'Error at {func_name}: {card2.__name__} : {e}')
        raise


def homepage():
    try:
        card1()
        card2()
    except Exception as e:
        raise

homepage()