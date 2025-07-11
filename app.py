import streamlit as st
from streamlit_option_menu import option_menu
from database import create_connection
from auth.login import login_page
from utils.auth_utils import get_user_by_token
from views.guru import *
from views.kriteria import *
from views.penilaian import *
from views.perbandingan_kriteria import *
from views.perbandingan_subkriteria import *
from views.perangkingan import *
from views.user_management import show_user_management
from views.dashboard import show_dashboard

def get_token():
    return st.query_params.get("token", None)

def main():
    st.set_page_config(page_title="Sistem AHP Penilaian Guru", layout="centered")
    token = get_token()
    
    if not token:
        login_page()
        return

    user = get_user_by_token(token)
    if not user:
        st.error("Token tidak valid atau sesi kadaluarsa.")
        login_page()
        return

    with st.sidebar:
        st.title("Welcome")
        st.write(f"👤 **{user['nama_lengkap']}** \n🛡️({user['role']})")
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

        if st.button("Logout"):
            st.query_params.clear()
            st.rerun()

    
    # Konten halaman sesuai menu
    st.title(f"{selected}")

    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Manajemen Guru":
        show_guru_page()
    elif selected == "Manajemen Kriteria":
        show_kriteria_page()
    elif selected == "Penilaian":
        show_penilaian_page()
    elif selected == "Perbandingan Kriteria":
        show_perbandingan_kriteria()
    elif selected == "Perbandingan Subkriteria":
        show_perbandingan_subkriteria()
    elif selected == "Perangkingan":
        show_hasil_perangkingan()
    elif selected == "Manajemen User":
        show_user_management()

if __name__ == "__main__":
    main()
