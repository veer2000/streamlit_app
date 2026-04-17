import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# ================= CONFIG =================
load_dotenv()

USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
HOST = os.getenv('DB_HOST')
DB   = os.getenv('DB_NAME')

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}"
)

st.set_page_config(layout="centered")
st.title("Summary of Responded Email")


# ================= LOAD DATA =================
@st.cache_data
def load_email_data():
    query = "SELECT user, status, email_timestamp FROM email_status_details"
    df = pd.read_sql(query, engine)

    df.columns = df.columns.str.strip()
    df["status"] = df["status"].astype(str).str.strip().str.lower()
    df["user"] = df["user"].astype(str).str.strip()

    if "email_timestamp" in df.columns:
        df["email_timestamp"] = pd.to_datetime(df["email_timestamp"], errors="coerce")

    return df


# ================= MAIN FUNCTION =================
def count_of_emails(start_date=None, end_date=None, run_filter=False):

    # call OF load_email_data -> res -> param for df
    df_res = load_email_data()
    temp_df = df_res.copy()

    # -------- FILTER --------
    if run_filter:
        if "email_timestamp" in temp_df.columns and start_date and end_date:
            temp_df = temp_df[
                (temp_df["email_timestamp"].dt.date >= start_date) &
                (temp_df["email_timestamp"].dt.date <= end_date)
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
    if not result.empty:
        col_left, col_center, col_right = st.columns([1, 2, 1])

        with col_center:
            fig, ax = plt.subplots(figsize=(5, 5))

            ax.pie(
                result["Completed_Emails"],
                labels=result["Username"],
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={'edgecolor': 'white'}
            )

            ax.set_title("Responded Emails", fontsize=14)
            st.pyplot(fig)

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


# ================= UI =================
df_ui = load_email_data()   # only for date range UI

date_col = "email_timestamp"

col1, col2, col3 = st.columns([1.5, 1.5, 1])

if date_col in df_ui.columns:
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
    start_date_null, end_date_null = None, None
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
            value=start_date_null,
            min_value=end_date_null,
            max_value=datetime.date.today(),
            label_visibility="collapsed"
        )

with col3:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    search_clicked = st.button("Search", use_container_width=True)


# ================= FUNCTION CALL =================
count_of_emails(
    start_date=start_date,
    end_date=end_date,
    run_filter=search_clicked
)