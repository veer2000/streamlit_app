import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import datetime

from Backend.src.services.database import SessionLocal
from Backend.src.services.model import EmailStatusDetail

db = SessionLocal()

@st.cache_data(ttl=30)
def load_data():
    try:
        with SessionLocal() as db_session:
            res = db_session.query(EmailStatusDetail).all()
        df_is = pd.DataFrame([row.to_dict() for row in res])
        date_columns = ['email_timestamp', 'start_time', 'end_time', 'created_time']
        for col in date_columns:
            if col in df_is.columns:
                df_is[col] = pd.to_datetime(df_is[col], errors='coerce')
        # print(f'from load_data of view_detailed_stats {df_is}')
        return df_is
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")

def get_date_column(df):
    if "start_time" in df.columns:
        return "start_time"

    if "email_timestamp" in df.columns:
        return "email_timestamp"

    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            return col

    return None

def apply_filters(df, target_user, start_date_view_detailes, end_view_detailes, selected_status, date_col):
    temp_df = df.copy()

    if target_user:
        temp_df = temp_df[temp_df["user"].str.contains(target_user, case=False, na=False)]

    if date_col:
        temp_df = temp_df[
            (temp_df[date_col].dt.date >= start_date_view_detailes) &
            (temp_df[date_col].dt.date <= end_view_detailes)
        ]

    if selected_status != "All":
        temp_df = temp_df[temp_df["status"] == selected_status]

    return temp_df

def style_status(val):
    val = str(val).lower()
    if val == "completed":
        return "color: green; font-weight: bold;"
    elif val in ["failed", "not started"]:
        return "color: red; font-weight: bold;"
    elif val == "processing":
        return "color: Yellow; font-weight: bold;"
    return ""


# ================= PREPARE DISPLAY =================
def prepare_display_df(df):
    display_df = df.copy()

    if "id" in display_df.columns:
        display_df = display_df.drop(columns=["id"])

    #
    if "user" in display_df.columns and "start_time" in display_df.columns:
        display_df = display_df.sort_values(
            by=["user", "start_time"],
            key=lambda col: col.str.lower() if col.name == "user" else col,
            ascending=[True, True]
        )

    display_df["id"] = range(1, len(display_df) + 1)

    if "msg_id" in display_df.columns:
        display_df["msg_id"] = display_df["msg_id"].astype(str).str[:25]

    display_df = display_df.drop(columns=['created_time'], errors='ignore')

    # Move ID first
    cols = ["id"] + [c for c in display_df.columns if c != "id"]
    display_df = display_df[cols]

    return display_df


def view_detailed_stats_logic():
    st.header("Email Database Management", text_alignment="center")
    df = load_data()

    if df.empty:
        st.warning("No data available")
        st.stop()

    if "display_df" not in st.session_state:
        st.session_state.display_df = df.copy()

    date_col = get_date_column(df)
    today = datetime.date.today()

    # session
    if "start_date_view_detailes" not in st.session_state:
        st.session_state.start_date_view_detailes = today

    if "end_view_detailes" not in st.session_state:
        st.session_state.end_view_detailes = today

    if st.session_state.end_view_detailes < st.session_state.start_date_view_detailes:
        st.session_state.end_view_detailes = st.session_state.start_date_view_detailes

    if "initialized" not in st.session_state:
        if date_col:
            st.session_state.display_df = df[
                df[date_col].dt.date == today
                ]
        else:
            st.session_state.display_df = df.copy()

        st.session_state.initialized = True
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1])

    with col1:
        st.markdown("**Enter a user**")
        target_user = st.text_input("User", placeholder="e.g Username", label_visibility="collapsed")

    if date_col:
        with col2:
            st.markdown("**Date From**")
            start_date_view_detailes = st.date_input(
                "Start",
                max_value=today,
                key="start_date_view_detailes",
                label_visibility="collapsed"
            )

        with col3:
            st.markdown("**Date To**")
            end_view_detailes = st.date_input(
                "End",
                max_value=today,
                key="end_view_detailes",
                label_visibility="collapsed"
            )
    else:
        start_date_view_detailes, end_view_detailes = None, None
        with col2:
            st.info("No date column")
        with col3:
            st.info("No date column")

    with col4:
        st.markdown("**Status**")
        status_options = ["All"] + sorted(df["status"].dropna().unique())
        selected_status = st.selectbox("Status", status_options, label_visibility="collapsed")

    with col5:
        st.markdown("**Action**")
        search_clicked = st.button("Search", use_container_width=True)

    # validate the end date is not before the start date
    # if date_col and end_view_detailes < start_date_view_detailes:
    #     st.error("End Date cannot be before Start Date")
    #     st.stop()

    # licked
    if search_clicked:
        filtered_df = apply_filters(df, target_user, start_date_view_detailes, end_view_detailes, selected_status, date_col)

        if target_user:
            st.metric(f"Total entries for '{target_user}'", len(filtered_df))

        st.session_state.display_df = filtered_df

    # Display
    display_df = prepare_display_df(st.session_state.display_df)

    if not display_df.empty:
        styled_df = display_df.style.map(style_status, subset=['status'])

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        if date_col and start_date_view_detailes == today and end_view_detailes == today:
            st.warning("No records found for today.")
        else:
            st.warning("No records found.")