import streamlit as st
from UI.utils.login_page import login_page_logic

def login_page_model():
    try:
        # 🔥 Apply CSS ONLY when login page is active
        # st.markdown("""
        # <style>
        # .main .block-container {
        #     display: flex;
        #     flex-direction: column;
        #     justify-content: center;
        #     height: 90vh;
        # }
        #
        # [data-testid="stVerticalBlockBorderWrapper"] {
        #     padding: 50px !important;
        #     border-radius: 15px;
        # }
        # </style>
        # """, unsafe_allow_html=True)
        login_page_logic()
    except Exception as e:
        raise
