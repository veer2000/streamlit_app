import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from matplotlib.ticker import MaxNLocator
import datetime
from Backend.src.services.database import SessionLocal
from Backend.src.services.model import EmailStatusDetail

today = datetime.date.today()
last_7_days = today - datetime.timedelta(days=7)

@st.cache_data(ttl=30)
def load_email_data():
    with SessionLocal() as db_session:
        res = db_session.query(EmailStatusDetail).all()

    df_is = pd.DataFrame([row.to_dict() for row in res])

    df_is.columns = df_is.columns.str.strip()
    df_is["status"] = df_is["status"].astype(str).str.strip().str.lower()
    df_is["user"] = df_is["user"].astype(str).str.strip()

    for col in df_is.columns:
        if "date" in col.lower() or "time" in col.lower():
            df_is[col] = pd.to_datetime(df_is[col], errors="coerce")

    return df_is


def get_filtered_data(df, start_date_view_stats, end_date_view_stats):
    return df[
        (df["end_time"].dt.date >= start_date_view_stats) &
        (df["end_time"].dt.date <= end_date_view_stats)
    ]


def build_pie_chart(result):
    fig, ax = plt.subplots(figsize=(5, 5))

    labels = [f"{u} ({c})" for u, c in zip(result["Username"], result["Completed_Emails"])]

    ax.pie(
        result["Completed_Emails"],
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white"}
    )

    ax.set_title("Responded Emails by User")
    st.pyplot(fig)


def build_bar_chart(df):
    daily = (
        df.groupby(df["end_time"].dt.date)
        .size()
        .reset_index(name="Count")
        .sort_values("end_time")
    )

    daily.columns = ["Date", "Count"]
    daily["Date_str"] = daily["Date"].apply(lambda x: x.strftime('%d-%b'))

    fig, ax = plt.subplots(figsize=(6, 5))

    x = range(len(daily))

    ax.bar(x, daily["Count"], edgecolor="black")
    ax.set_xticks(x)
    ax.set_xticklabels(daily["Date_str"], rotation=45)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_title("Responded Emails by Day")

    st.pyplot(fig)


def view_stats_logic():
    st.header("Emails Analytics Dashboard", text_alignment="center")
    try:
        df = load_email_data()

        if df.empty:
            st.warning("No data available")
            st.stop()

        if "end_time" not in df.columns:
            st.error("Column 'end_time' not found in data")
            st.stop()

        # ================= SESSION INIT =================
        if "start_date_view_stats" not in st.session_state:
            st.session_state.start_date_view_stats = last_7_days

        if "end_date_view_stats" not in st.session_state:
            st.session_state.end_date_view_stats = today

        if "filtered_df" not in st.session_state:
            st.session_state.filtered_df = df[
                (df["end_time"].dt.date >= last_7_days) &
                (df["end_time"].dt.date <= today)
            ]

        # ================= UI =================
        with st.form("filter_form"):

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                start_date_view_stats = st.date_input(
                    "Start Date",
                    key="start_date_view_stats",
                    max_value=today
                )

            with col2:
                end_date_view_stats = st.date_input(
                    "End Date",
                    key="end_date_view_stats",
                    max_value=today
                )

            with col3:
                st.markdown("")
                search = st.form_submit_button("Search", use_container_width=True)


        # ================= VALIDATION =================
        if end_date_view_stats < start_date_view_stats:
            st.error("End Date cannot be before Start Date")
            st.stop()

        # ================= SEARCH =================
        if search:
            filtered = get_filtered_data(df, start_date_view_stats, end_date_view_stats)
            st.session_state.filtered_df = filtered

        filtered_df = st.session_state.filtered_df

        completed_df = filtered_df[filtered_df["status"] == "completed"]

        if completed_df.empty:
            st.warning("No completed emails found for this range.")
            st.stop()

        result = (
            completed_df.groupby("user")
            .size()
            .reset_index(name="Completed_Emails")
            .rename(columns={"user": "Username"})
            .sort_values("Username")
        )

        # ================= CHARTS =================
        st.markdown("### Analytics")

        c1, c2 = st.columns(2)

        with c1:
            build_pie_chart(result)

        with c2:
            build_bar_chart(completed_df)

        # ================= TABLE =================
        st.markdown("### User Summary Table")
        st.dataframe(result, use_container_width=True, hide_index=True)

    except Exception as e:
        print(f'Error at view_stats_logic: {e}')
        raise