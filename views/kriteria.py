import streamlit as st
import pandas as pd
from utils.kriteria import *

def show_kriteria_page():
    tab1, tab2 = st.tabs(["📌 Kriteria", "📋 Subkriteria"])

    # ---------------- Kriteria ---------------- #
    with tab1:
        st.subheader("📌 Daftar Kriteria")
        kriteria_list = get_all_kriteria()
        if kriteria_list:
            df = pd.DataFrame(kriteria_list)
            df.index = df.index + 1
            df.index.name = "No"
            df.rename(columns={"nama_kriteria": "Nama Kriteria", "deskripsi": "Deskripsi"}, inplace=True)
            if "id_kriteria" in df.columns:
                df.drop(columns="id_kriteria", inplace=True)
            st.dataframe(df.style.set_properties(**{
                "text-align": "left",
                "font-size": "14px"
            }), use_container_width=True)
        else:
            st.info("Belum ada kriteria.")

        st.subheader("➕ Tambah Kriteria Baru")
        with st.form("form_kriteria"):
            nama = st.text_input("Nama Kriteria")
            deskripsi = st.text_area("Deskripsi")
            submitted = st.form_submit_button("Simpan")
            if submitted:
                if nama:
                    insert_kriteria(nama, deskripsi)
                    st.success("Kriteria berhasil ditambahkan.")
                    st.rerun()
                else:
                    st.warning("Nama kriteria wajib diisi.")

        if kriteria_list:
            st.subheader("🛠️ Edit / Hapus Kriteria")
            selected = st.selectbox("Pilih Kriteria", kriteria_list, format_func=lambda k: k["nama_kriteria"], key="select_kriteria_edit")
            new_nama = st.text_input("Edit Nama", selected["nama_kriteria"])
            new_desk = st.text_area("Edit Deskripsi", selected["deskripsi"])
            col1, col2 = st.columns(2)
            if col1.button("💾 Simpan Perubahan"):
                update_kriteria(selected["id_kriteria"], new_nama, new_desk)
                st.success("Kriteria berhasil diperbarui.")
                st.rerun()
            if col2.button("🗑️ Hapus Kriteria"):
                delete_kriteria(selected["id_kriteria"])
                st.success("Kriteria berhasil dihapus.")
                st.rerun()

    # ---------------- Subkriteria ---------------- #
    with tab2:
        st.subheader("📋 Manajemen Subkriteria")
        kriteria_list = get_all_kriteria()
        selected_kriteria = st.selectbox("Pilih Kriteria", kriteria_list, format_func=lambda x: x["nama_kriteria"], key="select_kriteria_sub")


        if selected_kriteria:
            subkriteria_list = get_subkriteria_by_kriteria(selected_kriteria["id_kriteria"])

            if subkriteria_list:
                df = pd.DataFrame(subkriteria_list)
                df.index = df.index + 1
                df.index.name = "No"
                df.rename(columns={"nama_subkriteria": "Nama Subkriteria", "deskripsi": "Deskripsi"}, inplace=True)
                if "id_subkriteria" in df.columns:
                    df.drop(columns="id_subkriteria", inplace=True)
                st.dataframe(df.style.set_properties(**{
                    "text-align": "left",
                    "font-size": "14px"
                }), use_container_width=True)
            else:
                st.info("Belum ada subkriteria untuk kriteria ini.")

            st.subheader("➕ Tambah Subkriteria")
            with st.form("form_sub"):
                nama_sub = st.text_input("Nama Subkriteria")
                deskripsi_sub = st.text_area("Deskripsi Subkriteria")
                submitted = st.form_submit_button("Tambah")
                if submitted:
                    if nama_sub:
                        insert_subkriteria(selected_kriteria["id_kriteria"], nama_sub, deskripsi_sub)
                        st.success("Subkriteria berhasil ditambahkan.")
                        st.rerun()
                    else:
                        st.warning("Nama subkriteria wajib diisi.")

            if subkriteria_list:
                st.subheader("🛠️ Edit / Hapus Subkriteria")
                selected_sub = st.selectbox("Pilih Subkriteria", subkriteria_list, format_func=lambda s: s["nama_subkriteria"], key="select_subkriteria")
                new_nama = st.text_input("Edit Nama Subkriteria", selected_sub["nama_subkriteria"], key="edit_sub_nama")
                new_desk = st.text_area("Edit Deskripsi", selected_sub["deskripsi"], key="edit_sub_desk")
                col1, col2 = st.columns(2)
                if col1.button("💾 Simpan Edit", key="edit_sub"):
                    update_subkriteria(selected_sub["id_subkriteria"], new_nama, new_desk)
                    st.success("Subkriteria berhasil diperbarui.")
                    st.rerun()
                if col2.button("🗑️ Hapus Subkriteria", key="hapus_sub"):
                    delete_subkriteria(selected_sub["id_subkriteria"])
                    st.success("Subkriteria berhasil dihapus.")
                    st.rerun()
