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
        print(f'from load_data of view_detailed_stats {df_is}')
        return df_is
        # convert all possible datetime columns
    #     for col in df.columns:
    #         if "date" in col.lower() or "time" in col.lower():
    #             df[col] = pd.to_datetime(df[col], errors="coerce")
    #
    #     return df
    #
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
    #     return pd.DataFrame()

def get_date_column(df):
    try:
        # priority
        if "email_timestamp" in df.columns:
            return "email_timestamp"

        # fallback: any date/time column
        for col in df.columns:
            if "date" in col.lower() or "time" in col.lower():
                return col

        return None
    except Exception as e:
        print(f' error at get_date_column {e}')
        raise

def apply_filters(df, target_user, start_date, end_date, selected_status, date_col):
    temp_df = df.copy()

    if target_user:
        temp_df = temp_df[temp_df["user"].str.contains(target_user, case=False, na=False)]

    if date_col and start_date and end_date:
        temp_df = temp_df[
            (temp_df[date_col].dt.date >= start_date) &
            (temp_df[date_col].dt.date <= end_date)
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
        return "color: orange; font-weight: bold;"
    return ""


# ================= PREPARE DISPLAY =================
def prepare_display_df(df):
    display_df = df.copy()

    if 'id' in display_df.columns:
        display_df['id'] = range(1, len(display_df) + 1)

    if "user" in display_df.columns:
        display_df = display_df.sort_values(by="user", key=lambda col: col.str.lower())

    if "msg_id" in display_df.columns:
        display_df["msg_id"] = display_df["msg_id"].astype(str).str[:25]

    display_df = display_df.drop(columns=['created_time'], errors='ignore')

    return display_df


def view_detailed_stats_logic():
    st.header("Detailed Stats", text_alignment="center")
    df = load_data()

    if df.empty:
        st.warning("No data available")
        st.stop()

    date_col = get_date_column(df)

    # ================= SESSION =================
    if 'display_df' not in st.session_state:
        st.session_state.display_df = df.copy()

    # ================= HEADER =================
    # top_spacer, top_btn_col = st.columns([8, 1])
    # with top_btn_col:
    #     if st.button("Back to DB", use_container_width=True):
    #         st.session_state.display_df = df.copy()
    #         st.rerun()

    # ================= UI =================
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1])

    with col1:
        st.markdown("**Enter a user**")
        target_user = st.text_input("Username search", placeholder="e.g. Username", label_visibility="collapsed")

    if date_col:
        if df[date_col].dtype == 'object':
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        min_date = df[date_col].min().date()
        max_date = df[date_col].max().date()

        with col2:
            st.markdown("**Date From**")
            start_date = st.date_input("S", value=min_date, label_visibility="collapsed")

        with col3:
            st.markdown("**Date To**")
            end_date = st.date_input("E", value=max_date, label_visibility="collapsed")
    else:
        start_date, end_date = None, None

        with col2:
            st.markdown("**Date From**")
            st.info("No date column")

        with col3:
            st.markdown("**Date To**")
            st.info("No date column")

    with col4:
        st.markdown("**Status**")
        status_options = ["All"] + sorted(df["status"].dropna().unique().tolist())
        selected_status = st.selectbox("Status", status_options, label_visibility="collapsed")

    with col5:
        st.markdown("**Action**")
        search_clicked = st.button("Search", use_container_width=True)

    # ================= CLICK =================
    if search_clicked:
        filtered_df = apply_filters(df, target_user, start_date, end_date, selected_status, date_col)

        if target_user:
            st.metric(label=f"Total entries for '{target_user}'", value=len(filtered_df))

        st.session_state.display_df = filtered_df

    # ================= DISPLAY =================
    display_df = prepare_display_df(st.session_state.display_df)

    if not display_df.empty:
        styled_df = display_df.style.applymap(style_status, subset=['status'])

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("id", width="small"),
                "msg_id": st.column_config.TextColumn("msg_id", width="medium")
            }
        )
    else:
        st.warning("No records found for those specific filters.")