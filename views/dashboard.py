import streamlit as st
from utils.db_functions import get_data

def show_dashboard():


    # Ambil data dari database
    guru_list = get_data("guru") or []
    kriteria_list = get_data("kriteria") or []
    subkriteria_list = get_data("subkriteria") or []
    user_list = get_data("user") or []

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Guru", len(guru_list))
    col2.metric("Jumlah Kriteria", len(kriteria_list))
    col3.metric("Jumlah Subkriteria", len(subkriteria_list))
    col4.metric("Jumlah User", len(user_list))

    st.markdown("---")
    st.write("Selamat datang di Sistem AHP untuk Penilaian Kenaikan Status Guru!")
