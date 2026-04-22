import streamlit as st
import pandas as pd
import pytz
from Backend.src.services.database import SessionLocal
from Backend.src.services.model import UserLogActivity
from datetime import datetime 

ist = pytz.timezone("Asia/Kolkata")
today = datetime.now(ist).date()


@st.cache_data(ttl=30)
def load_data():
    with SessionLocal() as db_session:
        res = db_session.query(UserLogActivity).all()

    df = pd.DataFrame([row.to_dict() for row in res])

    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def view_user_activity_logic():

    # ✅ ALWAYS INIT INSIDE FUNCTION
    if "start_date_user_log_act" not in st.session_state:
        st.session_state.start_date_user_log_act = today

    if "end_date_user_log_act" not in st.session_state:
        st.session_state.end_date_user_log_act = today

    if "selected_user_user_activity" not in st.session_state:
        st.session_state.selected_user_user_activity = "All"

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    st.header("User Activity Log", text_alignment="center")

    df_ui = load_data()
    if df_ui.empty:
        st.warning("No data available")
        st.stop()

    user_list = sorted(df_ui["user"].dropna().unique(), key=lambda x: x.lower())
    user_list.insert(0, "All")

    # ================= FORM =================
    with st.form("filter_form"):

        col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1])

        with col1:
            st.markdown("**Date From**")
            start_date_user_log_act = st.date_input(
                "Start",
                value=st.session_state.get("start_date_user_log_act", today),  # ✅ SAFE
                max_value=today,
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**Date To**")
            end_date_user_log_act = st.date_input(
                "End",
                value=st.session_state.get("end_date_user_log_act", today),  # ✅ SAFE
                max_value=today,
                label_visibility="collapsed"
            )

        with col3:
            st.markdown("**User**")
            selected_user_user_activity = st.selectbox(
                "User",
                options=user_list,
                index=user_list.index(
                    st.session_state.get("selected_user_user_activity", "All")  # ✅ SAFE
                ),
                label_visibility="collapsed"
            )

        with col4:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            submit = st.form_submit_button("Search", use_container_width=True)

        # ✅ MOVE THIS OUTSIDE col4 BUT INSIDE FORM
        if submit:
            st.session_state.start_date_user_log_act = start_date_user_log_act
            st.session_state.end_date_user_log_act = end_date_user_log_act
            st.session_state.selected_user_user_activity = selected_user_user_activity
            st.session_state.submitted = True

    # ================= FILTER =================
    df_res = load_data()
    filtered_df = df_res.copy()

    start_date_user_log_act = st.session_state.start_date_user_log_act
    end_date_user_log_act = st.session_state.end_date_user_log_act
    selected_user_user_activity = st.session_state.selected_user_user_activity

    if "log_in_time" in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df["log_in_time"].dt.date >= start_date_user_log_act) &
            (filtered_df["log_in_time"].dt.date <= end_date_user_log_act)
        ]

    if selected_user_user_activity != "All":
        filtered_df = filtered_df[
            filtered_df["user"] == selected_user_user_activity
        ]

    temp_df = filtered_df.copy()

    # ================= SORT =================
    if "log_in_time" in temp_df.columns:
        temp_df = temp_df.sort_values(by="log_in_time", ascending=True)

    if "user" in temp_df.columns:
        temp_df = temp_df.sort_values(
            by=["log_in_time", "user"],
            ascending=[True, True],
            key=lambda col: col.str.lower() if col.name == "user" else col
        )

    if not temp_df.empty:
        temp_df["id"] = range(1, len(temp_df) + 1)

    if "log_in_time" in temp_df.columns:
        temp_df["log_in_time"] = temp_df["log_in_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

    if "log_out_time" in temp_df.columns:
        temp_df["log_out_time"] = temp_df["log_out_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

    cols = ["id", "user", "log_in_time", "log_out_time",
            "is_logged_in", "device_id", "session_id", "type"]

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