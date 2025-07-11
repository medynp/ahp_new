import streamlit as st
import pandas as pd
from utils.guru import get_all_guru, insert_guru, update_guru, delete_guru, import_guru_excel

def show_guru_page():

    tab1, tab2, tab3 = st.tabs(["📋 Daftar Guru", "➕ Tambah Guru", "⬆️ Import Excel"])

    with tab1:
        st.subheader("📋 Daftar Guru")
        guru_list = get_all_guru()
        if guru_list:
            df = pd.DataFrame(guru_list)

            # Buat nomor urut dan ubah nama kolom
            df.index = df.index + 1
            df.index.name = "No"
            df = df.rename(columns={
                "nama_guru": "Nama Guru",
                "jabatan": "Jabatan"
            })
            if "id_guru" in df.columns:
                df.drop(columns="id_guru", inplace=True)

            # Tampilkan dengan gaya
            st.dataframe(
                df.style.set_properties(**{
                    "text-align": "left",
                    "font-size": "14px",
                    "border-color": "#d3d3d3"
                }),
                use_container_width=True
            )
        else:
            st.info("Belum ada data guru.")

        with st.expander("🛠️ Edit / Hapus Guru"):
            selected = st.selectbox("Pilih Guru", guru_list, format_func=lambda g: f"{g['nama_guru']} - {g['jabatan']}")
            if selected:
                nama_edit = st.text_input("Nama Guru", selected["nama_guru"])
                jabatan_edit = st.text_input("Jabatan", selected["jabatan"])
                col1, col2 = st.columns(2)
                if col1.button("💾 Simpan Perubahan"):
                    update_guru(selected["id_guru"], nama_edit, jabatan_edit)
                    st.success("Guru berhasil diperbarui")
                    st.rerun()
                if col2.button("🗑️ Hapus Guru"):
                    delete_guru(selected["id_guru"])
                    st.success("Guru berhasil dihapus")
                    st.rerun()

    with tab2:
        st.subheader("➕ Tambah Guru Baru")
        nama = st.text_input("Nama Guru")
        jabatan = st.text_input("Jabatan")
        if st.button("💾 Simpan"):
            if nama:
                insert_guru(nama, jabatan)
                st.success("Guru berhasil ditambahkan")
                st.rerun()
            else:
                st.warning("Nama tidak boleh kosong")

    with tab3:
        st.subheader("⬆️ Import Guru dari Excel")
        template = pd.DataFrame(columns=["nama_guru", "jabatan"])
        template.loc[0] = ["Contoh Guru", "Guru IPA"]
        st.download_button(
            label="📥 Download Template",
            data=template.to_csv(index=False).encode("utf-8"),
            file_name="template_guru.csv",
            mime="text/csv"
        )

        uploaded = st.file_uploader("Upload File Excel", type=["xlsx"])
        if uploaded:
            try:
                import_guru_excel(uploaded)
                st.success("Import berhasil!")
                st.rerun()
            except Exception as e:
                st.error(f"Gagal import: {e}")
