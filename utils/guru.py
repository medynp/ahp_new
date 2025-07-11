from database import create_connection
import pandas as pd

def get_all_guru():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guru")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return [dict(zip(col_names, row)) for row in rows]

def insert_guru(nama_guru, jabatan):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO guru (nama_guru, jabatan) VALUES (%s, %s)", (nama_guru, jabatan))
    conn.commit()
    cursor.close()

def update_guru(id_guru, nama_guru, jabatan):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE guru SET nama_guru = %s, jabatan = %s WHERE id_guru = %s", (nama_guru, jabatan, id_guru))
    conn.commit()
    cursor.close()

def delete_guru(id_guru):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guru WHERE id_guru = %s", (id_guru,))
    conn.commit()
    cursor.close()

def import_guru_excel(file):
    df = pd.read_excel(file)
    required_cols = {"nama_guru", "jabatan"}
    if not required_cols.issubset(df.columns):
        raise ValueError("File harus memiliki kolom: nama_guru, jabatan")

    conn = create_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        nama = str(row["nama_guru"]).strip()
        jabatan = str(row["jabatan"]).strip()

        # Lewati jika nama kosong
        if not nama:
            continue

        # Cek apakah nama sudah ada
        cursor.execute("SELECT COUNT(*) FROM guru WHERE nama_guru = %s", (nama,))
        exists = cursor.fetchone()[0]

        if exists == 0:
            cursor.execute(
                "INSERT INTO guru (nama_guru, jabatan) VALUES (%s, %s)",
                (nama, jabatan)
            )

    conn.commit()
    cursor.close()

