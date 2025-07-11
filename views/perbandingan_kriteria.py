import streamlit as st
import numpy as np
import pandas as pd
from utils.kriteria import get_all_kriteria
from utils.ahp import get_perbandingan_kriteria, save_perbandingan_kriteria, reset_perbandingan_kriteria, calculate_ahp

def show_perbandingan_kriteria():

    kriteria_list = get_all_kriteria()
    if len(kriteria_list) < 2:
        st.warning("Minimal harus ada 2 kriteria.")
        return

    id_map = {k['id_kriteria']: k['nama_kriteria'] for k in kriteria_list}
    id_list = list(id_map.keys())

    # Ambil perbandingan yang sudah ada
    data = get_perbandingan_kriteria()
    nilai_map = {}
    for d in data:
        nilai_map[(d[0], d[1])] = float(d[2])

    st.subheader("📝 Form Input Perbandingan")
    with st.form("form_perbandingan_kriteria"):
        input_nilai = {}
        for i in range(len(id_list)):
            for j in range(i+1, len(id_list)):
                id1 = id_list[i]
                id2 = id_list[j]
                default = round(nilai_map.get((id1, id2), 1.0), 2)

                nilai = st.select_slider(
                    f"{id_map[id1]} vs {id_map[id2]}",
                    options=[1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/2, 1/3, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    value=default if default in [1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/2, 1/3, 1, 2, 3, 4, 5, 6, 7, 8, 9] else 1,
                    format_func=lambda x: f"{x:.0f}" if x >= 1 else f"1/{round(1/x)}",
                    key=f"slider_{id1}_{id2}"
                )
                input_nilai[(id1, id2)] = nilai

        col1, col2 = st.columns(2)
        simpan = col1.form_submit_button("💾 Simpan")
        reset = col2.form_submit_button("🔄 Reset Semua")

    if simpan:
        for (id1, id2), nilai in input_nilai.items():
            save_perbandingan_kriteria(id1, id2, nilai)
            save_perbandingan_kriteria(id2, id1, 1 / nilai)
        st.success("Perbandingan berhasil disimpan.")
        st.rerun()

    if reset:
        reset_perbandingan_kriteria()
        st.success("Semua data dihapus.")
        st.rerun()

    # Tampilkan matriks & hasil AHP
    st.subheader("📈 Matriks & Bobot Kriteria")

    n = len(id_list)
    matrix = np.ones((n, n))

    # Isi matriks dari data
    for (i, id1) in enumerate(id_list):
        for (j, id2) in enumerate(id_list):
            if i == j:
                matrix[i][j] = 1.0
            elif (id1, id2) in nilai_map:
                matrix[i][j] = nilai_map[(id1, id2)]

    nama_list = [id_map[i] for i in id_list]
    result = calculate_ahp(matrix)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Matriks Perbandingan", "Normalisasi", "Bobot", "Konsistensi"
    ])

    with tab1:
        df_matrix = pd.DataFrame(matrix, index=nama_list, columns=nama_list)
        st.dataframe(df_matrix.style.format("{:.3f}"), use_container_width=True)


    with tab2:
        df_norm = pd.DataFrame(result['normalized_matrix'], index=nama_list, columns=nama_list)
        st.dataframe(df_norm.style.format("{:.3f}"), use_container_width=True)

    with tab3:
        df_bobot = pd.DataFrame({
            "Kriteria": nama_list,
            "Bobot": result["weights"],
            "Persen": (result["weights"] * 100).round(2)
        })
        st.dataframe(df_bobot.sort_values("Bobot", ascending=False), use_container_width=True)

    with tab4:
        AW = result["AW"]
        weights = result["weights"]
        AW_per_W = AW / weights

        df_aw = pd.DataFrame({
            "AW": AW,
            "W": weights,
            "AW/W": AW_per_W
        }, index=nama_list)
        st.dataframe(df_aw.style.format("{:.4f}"), use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("λ Maks", f"{result['lambda_max']:.4f}")
        col2.metric("CI", f"{result['ci']:.4f}")
        col3.metric("CR", f"{result['cr']:.4f}")

        if result['cr'] < 0.1:
            st.success("✅ Konsisten (CR < 0.1)")
        elif result['cr'] < 0.2:
            st.warning("⚠️ Cukup Konsisten (0.1 ≤ CR < 0.2)")
        else:
            st.error("❌ Tidak Konsisten (CR ≥ 0.2)")
