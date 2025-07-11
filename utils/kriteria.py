from database import create_connection

def get_all_kriteria():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kriteria")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return [dict(zip(col_names, row)) for row in rows]

def insert_kriteria(nama, deskripsi):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kriteria (nama_kriteria, deskripsi) VALUES (%s, %s)", (nama, deskripsi))
    conn.commit()
    cursor.close()

def update_kriteria(id_kriteria, nama, deskripsi):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE kriteria SET nama_kriteria=%s, deskripsi=%s WHERE id_kriteria=%s", (nama, deskripsi, id_kriteria))
    conn.commit()
    cursor.close()

def delete_kriteria(id_kriteria):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kriteria WHERE id_kriteria=%s", (id_kriteria,))
    conn.commit()
    cursor.close()

def get_subkriteria_by_kriteria(id_kriteria):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subkriteria WHERE id_kriteria=%s", (id_kriteria,))
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return [dict(zip(col_names, row)) for row in rows]

def insert_subkriteria(id_kriteria, nama, deskripsi):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subkriteria (id_kriteria, nama_subkriteria, deskripsi) VALUES (%s, %s, %s)", (id_kriteria, nama, deskripsi))
    conn.commit()
    cursor.close()

def update_subkriteria(id_sub, nama, deskripsi):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE subkriteria SET nama_subkriteria=%s, deskripsi=%s WHERE id_subkriteria=%s", (nama, deskripsi, id_sub))
    conn.commit()
    cursor.close()

def delete_subkriteria(id_sub):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subkriteria WHERE id_subkriteria=%s", (id_sub,))
    conn.commit()
    cursor.close()
