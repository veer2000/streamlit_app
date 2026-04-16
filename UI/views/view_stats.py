import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import datetime
from dotenv import load_dotenv

# ================= CONFIG =================
load_dotenv()

USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
HOST = os.getenv('DB_HOST')
DB   = os.getenv('DB_NAME')

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}"
)

# ================= PAGE =================
st.set_page_config(layout="centered")
st.title("Summary of Completed Email")


def load_data():
    query = "SELECT user, status, email_timestamp FROM email_status_details"
    return pd.read_sql(query, engine)

df = load_data()


df.columns = df.columns.str.strip()

df["status"] = df["status"].astype(str).str.strip().str.lower()
df["user"] = df["user"].astype(str).str.strip()

date_col = "email_timestamp"

if date_col in df.columns:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

# UI page column
col1, col2, col3 = st.columns([1.5, 1.5, 1])

if date_col in df.columns:
    with col1:
        st.markdown("**Date From**")
        start_date = st.date_input(
            "Start",
            value=df[date_col].min().date(),
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
    start_date, end_date = None, None,

with col3:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    search_clicked = st.button("Search", use_container_width=True)

# logic for clicked button
temp_df = df.copy()

if search_clicked:
    if date_col in temp_df.columns and start_date and end_date:
        temp_df = temp_df[
            (temp_df[date_col].dt.date >= start_date) & 
            (temp_df[date_col].dt.date <= end_date)
        ]


result = (
    temp_df[temp_df["status"] == "completed"]
    .groupby("user")
    .size()
    .reset_index(name="Completed_Emails")
)

result = (
    result.rename(columns={"user": "Username"})
    .sort_values(by="Completed_Emails", ascending=True)
)

#aligned table
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    if not result.empty:
        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True,   # removes 0,1,2
            height=(len(result) + 1) * 35  # removes extra empty space
        )
    else:
        st.warning("No records found.")