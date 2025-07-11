import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.ahp import *
from utils.kriteria import get_all_kriteria, get_subkriteria_by_kriteria
from utils.guru import get_all_guru
from utils.export_utils import *

def show_hasil_perangkingan():

    hasil, kriteria_cr, subkriteria_cr_map = calculate_total_scores()
    if not hasil:
        st.warning("Belum ada nilai guru yang dihitung.")
        return

    # 🔢 Tabel Ranking
    st.subheader("📋 Tabel Ranking Guru")
    df = pd.DataFrame(hasil)
    df["Peringkat"] = df["total_score"].rank(ascending=False).astype(int)
    df = df.sort_values("total_score", ascending=False)
    df_display = df[["Peringkat", "nama_guru", "total_score"]].rename(columns={
        "nama_guru": "Nama Guru", "total_score": "Total Skor"
    })
    st.dataframe(df_display.style.format({"Total Skor": "{:.4f}"}), use_container_width=True)

    
    # Tombol Download PDF
    pdf_buffer = export_ranking_to_pdf(hasil)
    st.download_button(
        label="📥 Download Hasil Perangkingan (PDF)",
        data=pdf_buffer,
        file_name="hasil_perangkingan_guru.pdf",
        mime="application/pdf"
    )
    
    # 📊 Visualisasi Batang
    st.subheader("📈 Visualisasi Total Skor")
    chart_data = df_display.set_index("Nama Guru")["Total Skor"]
    fig, ax = plt.subplots()
    bars = ax.bar(chart_data.index, chart_data.values, color=plt.cm.viridis(chart_data.values / max(chart_data.values)))

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f"{height:.2f}", ha='center', va='bottom', fontsize=8)

    ax.set_ylabel("Total Skor")
    ax.set_title("Skor Guru Berdasarkan AHP")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # 📌 Tabel Bobot Global Subkriteria
    st.subheader("📎 Bobot Global Subkriteria")
    kriteria_w, _, _ = get_kriteria_weights()
    sub_w, _ = get_subkriteria_weights()
    rows = []

    for k in get_all_kriteria():
        k_id = k["id_kriteria"]
        k_nama = k["nama_kriteria"]
        k_bobot = kriteria_w.get(k_id, 0)

        for sub in get_subkriteria_by_kriteria(k_id):
            s_id = sub["id_subkriteria"]
            s_nama = sub["nama_subkriteria"]
            s_bobot_lokal = sub_w.get(k_id, {}).get(s_id, 0)
            s_bobot_global = k_bobot * s_bobot_lokal

            rows.append({
                "Kriteria": k_nama,
                "Subkriteria": s_nama,
                "Bobot Lokal": s_bobot_lokal,
                "Bobot Global": s_bobot_global
            })

    df_bobot = pd.DataFrame(rows)
    st.dataframe(df_bobot.style.format({
        "Bobot Lokal": "{:.4f}", "Bobot Global": "{:.4f}"
    }), use_container_width=True)

    # 📏 Konsistensi Global
    st.subheader("📐 Analisis Konsistensi")

    col1, col2 = st.columns(2)
    col1.metric("CR Kriteria", f"{kriteria_cr:.4f}")
    col1.write("✅ Konsisten" if kriteria_cr < 0.1 else "⚠️ Perlu Diperiksa")

    if subkriteria_cr_map:
        rata_cr_sub = np.mean(list(subkriteria_cr_map.values()))
    else:
        rata_cr_sub = 0.0

    col2.metric("Rata-rata CR Subkriteria", f"{rata_cr_sub:.4f}")
    col2.write("✅ Konsisten" if rata_cr_sub < 0.1 else "⚠️ Perlu Diperiksa")

    # Detail CR per kriteria
    with st.expander("🔎 Detail CR per Kriteria"):
        for kid, cr in subkriteria_cr_map.items():
            k_name = next((k["nama_kriteria"] for k in get_all_kriteria() if k["id_kriteria"] == kid), f"Kriteria {kid}")
            status = "✅" if cr < 0.1 else "⚠️"
            st.write(f"{status} {k_name}: CR = {cr:.4f}")
