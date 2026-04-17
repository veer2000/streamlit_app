import streamlit as st
import pandas as pd
import os

from pandas import DataFrame
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()
st.set_page_config(layout="wide", page_title="Email Database")


USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

TABLE_NAME = "email_status_details"

# def load_data():
#     try:
#         engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASS}@{DB_HOST}/{DB_NAME}")
#         return pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)
#     except Exception as e:
#         st.error(f"❌ Connection Error: {e}")
#         return pd.DataFrame()
#
# df = load_data()

# if 'display_df' not in st.session_state:
#     st.session_state.display_df = df.copy()
#NOTE: need to return data fro db which is in table email_status_details
def view_detail_stats_logic():
    top_spacer, top_btn_col = st.columns([8, 1])
    with top_btn_col:
        # Clicking this button will now effectively "Restart" the app
        if st.button("Back to DB", use_container_width=True):
            st.session_state.display_df = df.copy()  # Wipe filters
            st.rerun()  # Force immediate refresh

    date_col = "email_timestamp"
    user_col = "user"

    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # SESSIon
    if 'display_df' not in st.session_state:
        st.session_state.display_df = df.copy()

    st.title("Email Database Management")

    # --- UI LAYOUT ---
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1.5, 1])

    with col1:
        st.markdown("**Enter a user**")
        target_user = st.text_input("Username search", placeholder="e.g. Username", label_visibility="collapsed")

    if date_col in df.columns:
        with col2:
            st.markdown("**Date From**")
            start_date = st.date_input("S", value=df[date_col].min().date(), label_visibility="collapsed")
        with col3:
            st.markdown("**Date To**")
            end_date = st.date_input("E", value=df[date_col].max().date(), label_visibility="collapsed")
    else:
        start_date, end_date = None, None

    with col4:
        st.markdown("**Status**")
        status_options = ["All"] + sorted(df["status"].dropna().unique().tolist())
        selected_status = st.selectbox("Status", status_options, label_visibility="collapsed")

    with col5:
        st.markdown("**Action**")
        search_clicked = st.button("Search", use_container_width=True)

    # --- LOGIC ---
    if search_clicked:
        temp_df = df.copy()

        if target_user and user_col in temp_df.columns:
            temp_df = temp_df[temp_df[user_col].str.contains(target_user, case=False, na=False)]
            st.metric(label=f"Total entries for '{target_user}'", value=len(temp_df))

        if date_col in temp_df.columns and start_date and end_date:
            temp_df = temp_df[
                (temp_df[date_col].dt.date >= start_date) &
                (temp_df[date_col].dt.date <= end_date)
                ]

        if selected_status != "All":
            temp_df = temp_df[temp_df["status"] == selected_status]

        # Save the filtered data to session state
        st.session_state.display_df = temp_df

    # --- RENDERING ---
    def style_status(val):
        val = str(val).lower()
        if val == "completed":
            return "color: green; font-weight: bold;"
        elif val in ["failed", "not started"]:
            return "color: red; font-weight: bold;"
        elif val in ["processing"]:
            return "color: yellow; font-weight: bold;"
        return ""

    # Always use the session state data for display
    display_df = st.session_state.display_df

    if not display_df.empty:
        if 'id' in display_df.columns:
            display_df['id'] = display_df['id'].astype(str)

        # Truncate msg_id to 15 strictly
        if "msg_id" in display_df.columns:
            display_df["msg_id"] = display_df["msg_id"].astype(str).str[:25]

        output_df = display_df.drop(columns=['created_time'], errors='ignore')

        styled_df = output_df.style.applymap(style_status,
                                             subset=['status']) if "status" in output_df.columns else output_df

        # Using column_config to ensure the ID column is tight and has no formatting
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("id", width="small"),
                "msg_id": st.column_config.TextColumn("Message ID", width="medium")
            }
        )
    else:
        st.warning("No records found for those specific filters.")