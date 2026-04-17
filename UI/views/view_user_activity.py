import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import datetime

# ================= CONFIG =================
st.set_page_config(layout="wide")
load_dotenv()

USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")
DB   = os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}")

# ================= CACHE DATA =================
@st.cache_data
def load_data():
    query = "SELECT * FROM streamlit.user_log_activity"
    df = pd.read_sql(query, engine)
    df["log_in_time"] = pd.to_datetime(df["log_in_time"], errors="coerce")
    df["log_out_time"] = pd.to_datetime(df["log_out_time"], errors="coerce")
    return df

df = load_data()

if df.empty:
    st.warning("No data available")
    st.stop()

# ================= DATE RANGE =================
date_col = "log_in_time"

min_date = df[date_col].dropna().min()
max_date = df[date_col].dropna().max()

if pd.isna(min_date) or pd.isna(max_date):
    st.error("Invalid date data")
    st.stop()

min_db_date = min_date.date()
today = datetime.date.today()

# ================= USER LIST =================
user_list = sorted(df["user"].dropna().unique())
user_list.insert(0, "All")


def view_user_activity_logic():
    # ================= UI LAYOUT =================
    left, center, right = st.columns([1, 4, 1])

    with center:
        st.markdown("<h1 style='text-align:left;'>User Log Activity</h1>", unsafe_allow_html=True)

        # ================= FORM =================
        with st.form("filter_form"):

            col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1])

            with col1:
                st.markdown("**Date From**")
                start_date = st.date_input(
                    "Start",
                    value=min_db_date,
                    min_value=min_db_date,
                    max_value=today,
                    label_visibility="collapsed"
                )

            with col2:
                st.markdown("**Date To**")
                end_date = st.date_input(
                    "End",
                    value=today,
                    min_value=start_date,
                    max_value=today,
                    label_visibility="collapsed"
                )

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

        # ================= FILTER LOGIC =================
        filtered_df = df.copy()

        if submit:
            filtered_df = filtered_df[
                (filtered_df[date_col].dt.date >= start_date) &
                (filtered_df[date_col].dt.date <= end_date)
                ]

            if selected_user != "All":
                filtered_df = filtered_df[
                    filtered_df["user"] == selected_user
                    ]

        # ================= FORMAT TABLE =================
        temp_df = filtered_df.copy()

        if "user" in temp_df.columns:
            temp_df = temp_df.sort_values(by="user", key=lambda col: col.str.lower())

        if not temp_df.empty:
            temp_df["id"] = range(1, len(temp_df) + 1)

        temp_df["log_in_time"] = temp_df["log_in_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        temp_df["log_out_time"] = temp_df["log_out_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

        cols = ["id", "user", "log_in_time", "log_out_time", "is_logged_in", "device_id", "session_id", "type"]
        temp_df = temp_df[[c for c in cols if c in temp_df.columns]]

        # Dynamic table height
        row_height = 35
        table_height = min(len(temp_df) * row_height + 40, 600)

        # ================= DISPLAY =================
        st.dataframe(
            temp_df,
            use_container_width=True,
            hide_index=True,
            height=table_height
        )