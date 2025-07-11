import streamlit as st
import pandas as pd
from datetime import datetime
from utils.kriteria import get_all_kriteria, get_subkriteria_by_kriteria
from utils.penilaian import get_nilai_guru, insert_or_update_nilai, delete_all_nilai_by_guru, import_nilai_excel
from utils.guru import get_all_guru
from io import BytesIO


def show_penilaian_page():

    guru_list = get_all_guru()
    if not guru_list:
        st.warning("Belum ada data guru.")
        return

    tab1, tab2 = st.tabs(["Input Manual", "Import Excel"])

    # ---------------- Tab 1 ----------------
    with tab1:
        selected_guru = st.selectbox(
            "Pilih Guru",
            guru_list,
            format_func=lambda g: g["nama_guru"],
            key="select_guru_penilaian"
        )

        st.subheader("📋 Data Penilaian Saat Ini")
        nilai_terisi = get_nilai_guru(selected_guru["id_guru"])
        if nilai_terisi:
            df = pd.DataFrame(nilai_terisi)[["nama_subkriteria", "nilai", "tanggal_penilaian"]]
            df.columns = ["Subkriteria", "Nilai", "Tanggal"]
            df.index = df.index + 1
            df.index.name = "No"
            st.dataframe(df, use_container_width=True)

            if st.button("🗑️ Hapus Semua Penilaian Guru Ini", key="hapus_semua"):
                delete_all_nilai_by_guru(selected_guru["id_guru"])
                st.success("Semua penilaian telah dihapus.")
                st.rerun()
        else:
            st.info("Belum ada data penilaian untuk guru ini.")

        st.subheader("🧾 Form Penilaian")

        kriteria_list = get_all_kriteria()
        nilai_dict = {}

        with st.form("form_input_nilai"):
            for kriteria in kriteria_list:
                st.markdown(f"**🔸 {kriteria['nama_kriteria']}**")
                sub_list = get_subkriteria_by_kriteria(kriteria["id_kriteria"])
                if not sub_list:
                    st.warning(f"Tidak ada subkriteria untuk {kriteria['nama_kriteria']}")
                    continue

                for sub in sub_list:
                    nilai = st.number_input(
                        f"{sub['nama_subkriteria']} (1–5)",
                        min_value=1, max_value=5, step=1,
                        key=f"nilai_{selected_guru['id_guru']}_{sub['id_subkriteria']}"
                    )
                    nilai_dict[sub["id_subkriteria"]] = nilai

            submitted = st.form_submit_button("💾 Simpan Penilaian")
            if submitted:
                for sub_id, nilai in nilai_dict.items():
                    insert_or_update_nilai(selected_guru["id_guru"], sub_id, nilai)
                st.success("✅ Penilaian berhasil disimpan.")
                st.rerun()

    # ---------------- Tab 2 ----------------
    with tab2:
        st.subheader("⬆️ Import Penilaian dari Excel")

        if st.button("📄 Download Template"):
            sub_names = []
            for k in get_all_kriteria():
                sub_names += [s["nama_subkriteria"] for s in get_subkriteria_by_kriteria(k["id_kriteria"])]

            data = {
                "nama_guru": ["Contoh Guru"],
                "tanggal_penilaian": [datetime.now().date()]
            }
            for sub in sub_names:
                data[sub] = [3]

            df_template = pd.DataFrame(data)
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df_template.to_excel(writer, index=False, sheet_name="Data_Nilai")

            st.download_button(
                label="⬇️ Download Template Excel",
                data=buffer.getvalue(),
                file_name="template_penilaian.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        uploaded = st.file_uploader("Upload File Excel", type=["xlsx"])

        if uploaded:
            try:
                import_nilai_excel(uploaded)
                st.success("✅ Data penilaian berhasil diimpor.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Gagal import: {e}")
