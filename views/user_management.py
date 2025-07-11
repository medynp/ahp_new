import streamlit as st
import pandas as pd
from utils.user_management import (
    get_all_users,
    create_user,
    update_user_role,
    delete_user
)

def show_user_management():

    user_list = get_all_users()
    if not user_list:
        st.warning("Belum ada data user.")
        return

    # Tampilkan Tabel User
    df = pd.DataFrame(user_list)
    df_view = df[["id_user", "nama_lengkap", "username", "role"]].rename(columns={
        "id_user": "ID",
        "nama_lengkap": "Nama Lengkap",
        "username": "Email",
        "role": "Level Akses"
    })
    st.subheader("📋 Daftar Pengguna")
    st.dataframe(df_view, use_container_width=True)

    # Form Tambah User
    st.subheader("➕ Tambah Akun Baru")
    with st.form("form_tambah_user"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap")
            email = st.text_input("Email (Username)")
        with col2:
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["admin", "user"])

        submitted = st.form_submit_button("Tambah User")
        if submitted:
            result = create_user(nama, email, password, role)
            if result == "success":
                st.success("Akun berhasil ditambahkan!")
                st.rerun()
            elif result == "username_exists":
                st.warning("Email sudah terdaftar.")
            elif result == "email_invalid":
                st.warning("Format email tidak valid.")
            else:
                st.error("Gagal menambahkan user.")

    # Ubah Role
    st.subheader("🔧 Ubah Role Pengguna")
    selected_user = st.selectbox("Pilih User", user_list, format_func=lambda u: f"{u['nama_lengkap']} ({u['username']})", key="ubah_role_user")
    new_role = st.selectbox("Pilih Role Baru", ["admin", "user"], index=["admin", "user"].index(selected_user['role']))
    if st.button("Update Role"):
        if update_user_role(selected_user['id_user'], new_role):
            st.success("Role berhasil diupdate!")
            st.rerun()
        else:
            st.error("Gagal mengupdate role.")

    # Hapus User
    st.subheader("🗑️ Hapus Pengguna")
    user_to_delete = st.selectbox("Pilih User yang Dihapus", user_list, format_func=lambda u: f"{u['nama_lengkap']} ({u['username']})", key="hapus_user_select")
    if st.button("Hapus User"):
        if delete_user(user_to_delete['id_user']):
            st.success("User berhasil dihapus.")
            st.rerun()
        else:
            st.error("Gagal menghapus user.")
