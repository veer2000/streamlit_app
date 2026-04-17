import plt
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import datetime
from dotenv import load_dotenv

from Backend.src.services.database import SessionLocal
from Backend.src.services.model import EmailStatusDetail

db = SessionLocal()

@st.cache_data(ttl=30)
def load_email_data():
    with SessionLocal() as db_session:
        res = db_session.query(EmailStatusDetail).all()
    df_is = pd.DataFrame([row.to_dict() for row in res])
    # query = "SELECT user, status, email_timestamp FROM email_status_details"
    # df = pd.read_sql(query, engine)

    df_is.columns = df_is.columns.str.strip()
    df_is["status"] = df_is["status"].astype(str).str.strip().str.lower()
    df_is["user"] = df_is["user"].astype(str).str.strip()

    # convert all possible datetime columns
    for col in df_is.columns:
        if "date" in col.lower() or "time" in col.lower():
            df_is[col] = pd.to_datetime(df_is[col], errors="coerce")

    return df_is


def view_stats_logic():
    try:
        st.header("View Stats", text_alignment="center")
        # ================= UI =================
        df_ui = load_email_data()

        # -------- AUTO DETECT DATE COLUMN --------
        date_col = None
        for col in df_ui.columns:
            if "date" in col.lower() or "time" in col.lower():
                date_col = col
                break

        col1, col2, col3 = st.columns([1.5, 1.5, 1])

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
                st.info("No date column available")

            with col2:
                st.markdown("**Date To**")
                st.info("No date column available")

        with col3:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            search_clicked = st.button("Search", use_container_width=True)

        df_res = load_email_data()
        temp_df = df_res.copy()

        # -------- FILTER --------
        if search_clicked and date_col and start_date and end_date:
            temp_df = temp_df[
                (temp_df[date_col].dt.date >= start_date) &
                (temp_df[date_col].dt.date <= end_date)
                ]

        # -------- SUMMARY --------
        completed_df = temp_df[temp_df["status"] == "completed"]

        result = (
            completed_df.groupby("user")
            .size()
            .reset_index(name="Completed_Emails")
        )

        if not result.empty:
            result = result.rename(columns={"user": "Username"})
            result = result.sort_values(by="Username")

        # -------- PIE CHART --------
        # if not result.empty:
        #     col_left, col_center, col_right = st.columns([1, 2, 1])
        #
        #     with col_center:
        #         fig, ax = plt.subplots(figsize=(5, 5))
        #
        #         labels = [
        #             f"{user} ({count})"
        #             for user,
        #             count in zip(result["Username"],
        #                          result["Completed_Emails"])
        #         ]
        #
        #         ax.pie(
        #             result["Completed_Emails"],
        #             labels=labels,
        #             autopct="%1.1f%%",
        #             startangle=90,
        #             wedgeprops={'edgecolor': 'white'}
        #         )
        #
        #         ax.set_title("Responded Emails", fontsize=14)
        #         st.pyplot(fig)

        # -------- TABLE --------
        if not result.empty:
            col_left, col_center, col_right = st.columns([0.5, 3, 0.5])

            with col_center:
                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True,
                    height=min(800, (len(result) + 1) * 35),
                    column_config={
                        "Username": st.column_config.TextColumn("Username", width="medium"),
                        "Completed_Emails": st.column_config.NumberColumn("Count", width="small")
                    }
                )
        else:
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                st.warning("No records found.")

    except Exception as e:
        print(f"\033[91mError is {e}\033[0m")