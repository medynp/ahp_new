import streamlit as st
from streamlit_option_menu import option_menu

def sidebar_menu(user):
    st.sidebar.title("🧑‍🏫 Sistem AHP")

    st.sidebar.markdown(f"👤 **{user['nama_lengkap']}**  \n🛡️ _{user['role'].capitalize()}_")
    st.sidebar.markdown("---")

    if user["role"] == "admin":
        selected = option_menu(
            menu_title="Menu Utama",
            options=[
                "Dashboard",
                "Manajemen Guru",
                "Manajemen Kriteria",
                "Penilaian",
                "Perbandingan Kriteria",
                "Perbandingan Subkriteria",
                "Perangkingan",
                "Manajemen User",
            ],
            icons=[
                "house",
                "people",
                "list-task",
                "clipboard-check",
                "bar-chart",
                "bar-chart-line",
                "bar-chart-steps",
                "people",
            ],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "5px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#f0f2f6",
                },
                "nav-link-selected": {
                    "background-color": "#4a90e2",
                    "color": "white",
                    "font-weight": "bold",
                },
            },
        )
    else:
        selected = option_menu(
            menu_title="Menu Utama",
            options=["Perangkingan"],
            icons=["bar-chart-steps"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#f0f2f6",
                },
                "nav-link-selected": {
                    "background-color": "#4a90e2",
                    "color": "white",
                    "font-weight": "bold",
                },
            },
        )

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", key="logout_button"):
        st.session_state.clear()
        st.rerun()

    return selected
