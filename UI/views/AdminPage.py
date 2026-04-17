import streamlit as st
from UI.views.manage_priority import manage_page_logic
# from UI.views.view_detailed_stats import view_detail_stats_logic
# from UI.views.view_stats import view_stats_logic
# from UI.views.view_user_activity import view_user_activity_logic
from Backend.src.services.curd import retrieve_drop_down_menu, retrieve_drop_down_of_users, retrieve_drop_down_menu_for_user, \
    add_priority_data_to_user
from Backend.src.services.database import SessionLocal
from Backend.src.services.utils import on_user_change, mark_change, validate_priorities, show_unsaved_changes_modal, \
    reset_priorities

if "admin_page_default" not in st.session_state:
    st.session_state.admin_page_default = True

if "admin_tab" not in st.session_state:
    st.session_state.admin_tab = "manage"

def admin_page_logic():
    left_spacer, center_col, right_spacer = st.columns([1.5, 5, 1])

    with center_col:
        if st.session_state.admin_tab == "manage":
            manage_page_logic()

        elif st.session_state.admin_tab == "activity":
            # view_user_activity_logic()
            st.write('view_user_activity_logic called')

        elif st.session_state.admin_tab == "stats":
            # view_stats_logic()
            st.write('view_stats_logic called')

        elif st.session_state.admin_tab == "detailed":
            # view_detail_stats_logic()
            st.write('view_detail_stats_logic called')
