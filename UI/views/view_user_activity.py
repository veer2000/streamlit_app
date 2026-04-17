import streamlit as st
import pandas as pd

from Backend.src.services.database import SessionLocal
from Backend.src.services.model import UserLogActivity
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import datetime

db = SessionLocal()

@st.cache_data(ttl=30)
def load_data():
    try:
        # query = "SELECT * FROM streamlit.user_log_activity"
        # df = pd.read_sql(query, engine)
        with SessionLocal() as db_session:
            res = db_session.query(UserLogActivity).all()
        df_is = pd.DataFrame([row.to_dict() for row in res])
        print(f'res form Load_data is {df_is}')
        for col in df_is.columns:
            if "date" in col.lower() or "time" in col.lower():
                df_is[col] = pd.to_datetime(df_is[col], errors="coerce")

        return df_is
    except Exception as e:
        print(f'error at load_data: {e}')
        raise

def view_user_activity_logic():
    st.header("User Activity Log", text_alignment="center")
    df_ui = load_data()
    if df_ui.empty:
        st.warning("No data available")
        st.stop()

    date_col = None
    for col in df_ui.columns:
        if "date" in col.lower() or "time" in col.lower():
            date_col = col
            break

    user_list = sorted(df_ui["user"].dropna().unique())
    user_list.insert(0, "All")

    with st.form("filter_form"):

        col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1])

        if date_col:
            with col1:
                st.markdown("**Date From**")
                start_date = st.date_input(
                    "Start",
                    value=df_ui[date_col].min().date(),
                    label_visibility="collapsed"
                )

            with col2:
                st.markdown("**Date To**")
                end_date = st.date_input(
                    "End",
                    value=start_date,
                    min_value=start_date,
                    max_value=datetime.date.today(),
                    label_visibility="collapsed"
                )
        else:
            start_date, end_date = None, None

            with col1:
                st.markdown("**Date From**")
                st.info("No date column found")

            with col2:
                st.markdown("**Date To**")
                st.info("No date column found")

        with col3:
            st.markdown("**User**")
            selected_user = st.selectbox(
                "User",
                options=user_list,
                label_visibility="collapsed"
            )

        with col4:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            submit = st.form_submit_button("Search", use_container_width=True)

        # filtered_df = df_ui.copy()

        if submit and date_col and start_date and end_date:
            df_ui = df_ui[
                (df_ui[date_col].dt.date >= start_date) &
                (df_ui[date_col].dt.date <= end_date)
                ]

            if selected_user != "All":
                df_ui = df_ui[
                    df_ui["user"] == selected_user
                    ]

        temp_df = df_ui.copy()

        if "user" in temp_df.columns:
            temp_df = temp_df.sort_values(by="user", key=lambda col: col.str.lower())

        if not temp_df.empty:
            temp_df["id"] = range(1, len(temp_df) + 1)

        # format only if column exists
        if "log_in_time" in temp_df.columns:
            temp_df["log_in_time"] = temp_df["log_in_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

        if "log_out_time" in temp_df.columns:
            temp_df["log_out_time"] = temp_df["log_out_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

        cols = ["id", "user", "log_in_time", "log_out_time", "is_logged_in", "device_id", "session_id", "type"]
        temp_df = temp_df[[c for c in cols if c in temp_df.columns]]

        if not temp_df.empty:
            row_height = 35
            table_height = min(len(temp_df) * row_height + 40, 600)

            st.dataframe(
                temp_df,
                use_container_width=True,
                hide_index=True,
                height=table_height
            )
        else:
            st.warning("No records found.")
