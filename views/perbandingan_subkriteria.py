import streamlit as st
import numpy as np
import pandas as pd
from utils.kriteria import get_all_kriteria, get_subkriteria_by_kriteria
from utils.ahp import (
    get_perbandingan_subkriteria,
    save_perbandingan_subkriteria,
    reset_perbandingan_subkriteria,
    calculate_ahp
)

def show_perbandingan_subkriteria():

    kriteria_list = get_all_kriteria()
    selected_kriteria = st.selectbox(
        "Pilih Kriteria",
        options=kriteria_list,
        format_func=lambda k: k["nama_kriteria"],
        key="select_kriteria_sub"
    )

    if not selected_kriteria:
        return

    id_kriteria = selected_kriteria["id_kriteria"]
    subkriteria_list = get_subkriteria_by_kriteria(id_kriteria)

    if len(subkriteria_list) < 2:
        st.warning("Subkriteria untuk kriteria ini belum cukup (minimal 2).")
        return

    id_map = {s['id_subkriteria']: s['nama_subkriteria'] for s in subkriteria_list}
    id_list = list(id_map.keys())

    # Ambil data perbandingan sebelumnya
    data = get_perbandingan_subkriteria(id_kriteria)
    nilai_map = {}
    for d in data:
        nilai_map[(d[1], d[2])] = float(d[3])

    st.subheader("📝 Input Perbandingan Subkriteria")
    with st.form("form_subkriteria"):
        input_nilai = {}
        for i in range(len(id_list)):
            for j in range(i+1, len(id_list)):
                id1 = id_list[i]
                id2 = id_list[j]
                default = round(nilai_map.get((id1, id2), 1.0), 2)

                nilai = st.select_slider(
                    f"{id_map[id1]} vs {id_map[id2]}",
                    options=[0.11, 0.125, 0.14, 0.17, 0.20, 0.25, 0.33, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
                    value=default if default in [0.11, 0.125, 0.14, 0.17, 0.20, 0.25, 0.33, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0] else 1.0,
                    format_func=lambda x: f"{x:.2f}" if x < 1 else f"{int(x)}",
                    key=f"slider_{id1}_{id2}"
                )
                input_nilai[(id1, id2)] = nilai

        col1, col2 = st.columns(2)
        simpan = col1.form_submit_button("💾 Simpan")
        reset = col2.form_submit_button("🔄 Reset")

    if simpan:
        for (id1, id2), nilai in input_nilai.items():
            save_perbandingan_subkriteria(id_kriteria, id1, id2, nilai)
            save_perbandingan_subkriteria(id_kriteria, id2, id1, 1 / nilai)
        st.success("Perbandingan disimpan.")
        st.rerun()

    if reset:
        reset_perbandingan_subkriteria(id_kriteria)
        st.success("Semua perbandingan dihapus.")
        st.rerun()

    # Tampilkan Matriks AHP
    st.subheader("📈 Hasil Perbandingan Subkriteria")

    n = len(id_list)
    matrix = np.ones((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                id1, id2 = id_list[i], id_list[j]
                matrix[i][j] = nilai_map.get((id1, id2), 1.0)

    nama_list = [id_map[i] for i in id_list]
    result = calculate_ahp(matrix)

    tab1, tab2, tab3, tab4 = st.tabs(["Matriks", "Normalisasi", "Bobot", "Konsistensi"])

    with tab1:
        df_matrix = pd.DataFrame(matrix, index=nama_list, columns=nama_list)
        st.dataframe(df_matrix.style.format("{:.2f}"), use_container_width=True)

    with tab2:
        df_norm = pd.DataFrame(result['normalized_matrix'], index=nama_list, columns=nama_list)
        st.dataframe(df_norm.style.format("{:.3f}"), use_container_width=True)

    with tab3:
        df_bobot = pd.DataFrame({
            "Subkriteria": nama_list,
            "Bobot": result["weights"],
            "Persen": (result["weights"] * 100).round(2)
        })
        st.dataframe(df_bobot.sort_values("Bobot", ascending=False), use_container_width=True)

    with tab4:
        st.metric("λ Max", f"{result['lambda_max']:.4f}")
        st.metric("CI", f"{result['ci']:.4f}")
        st.metric("CR", f"{result['cr']:.4f}")

        if result["cr"] < 0.1:
            st.success("✅ Konsisten")
        elif result["cr"] < 0.2:
            st.warning("⚠️ Cukup Konsisten")
        else:
            st.error("❌ Tidak Konsisten")

