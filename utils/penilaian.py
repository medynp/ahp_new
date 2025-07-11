from database import create_connection
import pandas as pd
from datetime import datetime

def get_nilai_guru(guru_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ns.*, s.nama_subkriteria 
        FROM nilai_subkriteria ns 
        JOIN subkriteria s ON ns.id_subkriteria = s.id_subkriteria
        WHERE ns.id_guru = %s
    """, (guru_id,))
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    return [dict(zip(columns, row)) for row in rows]

def get_nilai_by_guru_sub(guru_id, sub_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM nilai_subkriteria
        WHERE id_guru = %s AND id_subkriteria = %s
    """, (guru_id, sub_id))
    row = cursor.fetchone()
    cursor.close()
    return row

def insert_or_update_nilai(guru_id, sub_id, nilai):
    from datetime import datetime
    conn = create_connection()
    cursor = conn.cursor()
    existing = get_nilai_by_guru_sub(guru_id, sub_id)
    if existing:
        cursor.execute("""
            UPDATE nilai_subkriteria 
            SET nilai = %s, tanggal_penilaian = %s 
            WHERE id_guru = %s AND id_subkriteria = %s
        """, (nilai, datetime.now().date(), guru_id, sub_id))
    else:
        cursor.execute("""
            INSERT INTO nilai_subkriteria (id_guru, id_subkriteria, nilai, tanggal_penilaian)
            VALUES (%s, %s, %s, %s)
        """, (guru_id, sub_id, nilai, datetime.now().date()))
    conn.commit()
    cursor.close()

def delete_nilai(guru_id, subkriteria_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM nilai_subkriteria 
        WHERE id_guru = %s AND id_subkriteria = %s
    """, (guru_id, subkriteria_id))
    conn.commit()
    cursor.close()

def delete_all_nilai_by_guru(guru_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nilai_subkriteria WHERE id_guru = %s", (guru_id,))
    conn.commit()
    cursor.close()

def import_nilai_excel(file):
    import pandas as pd
    from utils.guru import get_all_guru
    from utils.kriteria import get_all_kriteria, get_subkriteria_by_kriteria
    from datetime import datetime

    df = pd.read_excel(file, sheet_name="Data_Nilai")
    if "nama_guru" not in df.columns or "tanggal_penilaian" not in df.columns:
        raise ValueError("Kolom 'nama_guru' dan 'tanggal_penilaian' wajib ada.")

    # Buat mapping nama guru ke ID
    guru_map = {g["nama_guru"]: g["id_guru"] for g in get_all_guru()}

    # Mapping nama subkriteria ke ID
    sub_map = {}
    for k in get_all_kriteria():
        for sub in get_subkriteria_by_kriteria(k["id_kriteria"]):
            sub_map[sub["nama_subkriteria"]] = sub["id_subkriteria"]

    nilai_data = []
    for _, row in df.iterrows():
        nama = str(row["nama_guru"]).strip()
        tanggal = pd.to_datetime(row["tanggal_penilaian"]).date()

        if nama not in guru_map:
            continue  # lewati jika guru tidak ditemukan

        for sub_nama, sub_id in sub_map.items():
            if sub_nama in row and pd.notna(row[sub_nama]):
                nilai = int(row[sub_nama])
                nilai_data.append((guru_map[nama], sub_id, nilai, tanggal))

    # Simpan ke database
    conn = create_connection()
    cursor = conn.cursor()

    for id_guru, id_sub, nilai, tanggal in nilai_data:
        cursor.execute("""
            SELECT id_nilai FROM nilai_subkriteria 
            WHERE id_guru=%s AND id_subkriteria=%s
        """, (id_guru, id_sub))
        exists = cursor.fetchone()

        if exists:
            cursor.execute("""
                UPDATE nilai_subkriteria 
                SET nilai=%s, tanggal_penilaian=%s 
                WHERE id_nilai=%s
            """, (nilai, tanggal, exists[0]))
        else:
            cursor.execute("""
                INSERT INTO nilai_subkriteria (id_guru, id_subkriteria, nilai, tanggal_penilaian)
                VALUES (%s, %s, %s, %s)
            """, (id_guru, id_sub, nilai, tanggal))

    conn.commit()
    cursor.close()
