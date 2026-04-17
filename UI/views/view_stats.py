import plt
import streamlit as st
import pandas as pd
from matplotlib.ticker import MaxNLocator

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


def get_filtered_data(df_ui, date_col, start_date, end_date, submit_clicked):
    df = df_ui.copy()

    if submit_clicked:
        df = df_ui[
            (df_ui[date_col].dt.date >= start_date) &
            (df_ui[date_col].dt.date <= end_date)
        ].copy()

    return df

def build_pie_chart(result):
    fig, ax = plt.subplots(figsize=(5, 5))

    labels = [
        f"{u} ({c})"
        for u, c in zip(result["Username"], result["Completed_Emails"])
    ]

    ax.pie(
        result["Completed_Emails"],
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white"}
    )

    ax.set_title("Responded Emails by User")
    st.pyplot(fig)

def build_bar_chart(completed_df, date_col):
    daily_counts = (
        completed_df
        .groupby(completed_df[date_col].dt.date)
        .size()
        .reset_index(name="Count")
    )

    daily_counts.columns = ["Date", "Count"]
    daily_counts = daily_counts.sort_values("Date")

    daily_counts["Date_str"] = daily_counts["Date"].apply(
        lambda x: x.strftime('%d-%b')
    )

    fig, ax = plt.subplots(figsize=(6, 5))

    x_pos = range(len(daily_counts))

    ax.bar(
        x_pos,
        daily_counts["Count"],
        width=0.6,
        edgecolor="black",
        color="#222222",
        alpha=0.8
    )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(daily_counts["Date_str"], rotation=45, fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_title("Responded Emails by Day")

    st.pyplot(fig)

def view_stats_logic():
    try:
        st.header("User Stats", text_alignment="center")
        df_ui = load_email_data()

        if df_ui.empty:
            st.warning("No data available")
            st.stop()

        date_col = "end_time"

        # ================= FILTER UI =================
        with st.form("filter_form"):

            col1, col2, col3 = st.columns([2, 2, 1])

            min_db_date = df_ui[date_col].min().date()
            max_db_date = df_ui[date_col].max().date()

            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=min_db_date,
                    format="YYYY/MM/DD"
                )

            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=max_db_date,
                    format="YYYY/MM/DD"
                )

            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                submit_button = st.form_submit_button(
                    "Search",
                    use_container_width=True
                )

        # ================= DATA PROCESSING =================
        df = get_filtered_data(df_ui, date_col, start_date, end_date, submit_button)

        completed_df = df[df["status"] == "completed"]

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

        c1, c2 = st.columns(2, gap="large")

        with c1:
            build_pie_chart(result)

        with c2:
            build_bar_chart(completed_df, date_col)

        # ================= TABLE =================
        st.markdown("### User Summary Table")
        st.dataframe(result, use_container_width=True, hide_index=True)
    except Exception as e:
        print(f"\033[91mError is {e}\033[0m")