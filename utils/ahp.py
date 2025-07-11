import numpy as np
from database import create_connection
from utils.guru import get_all_guru
from utils.kriteria import get_all_kriteria, get_subkriteria_by_kriteria

# Random Index (RI) untuk ukuran matriks 1–10
RI_TABLE = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

def calculate_ahp(matrix):
    n = len(matrix)

    # 1. Normalisasi kolom
    column_sums = np.sum(matrix, axis=0)
    normalized_matrix = matrix / column_sums

    # 2. Bobot (rata-rata baris normalisasi)
    weights = np.mean(normalized_matrix, axis=1)

    # 3. AW = matrix * weights
    AW = np.dot(matrix, weights)

    # 4. λmax = rata-rata (AW / W)
    lambda_max = np.mean(AW / weights)

    # 5. CI dan CR
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0
    ri = RI_TABLE.get(n, 1.49)
    cr = ci / ri if ri != 0 else 0

    return {
        "normalized_matrix": normalized_matrix,
        "weights": weights,
        "AW": AW,
        "lambda_max": lambda_max,
        "ci": ci,
        "cr": cr,
        "ri": ri
    }

def get_perbandingan_kriteria():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perbandingan_kriteria")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def save_perbandingan_kriteria(id1, id2, nilai):
    conn = create_connection()
    cursor = conn.cursor()

    # Cek apakah data sudah ada
    cursor.execute("""
        SELECT * FROM perbandingan_kriteria 
        WHERE id_kriteria1=%s AND id_kriteria2=%s
    """, (id1, id2))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE perbandingan_kriteria SET nilai_perbandingan=%s 
            WHERE id_kriteria1=%s AND id_kriteria2=%s
        """, (nilai, id1, id2))
    else:
        cursor.execute("""
            INSERT INTO perbandingan_kriteria (id_kriteria1, id_kriteria2, nilai_perbandingan)
            VALUES (%s, %s, %s)
        """, (id1, id2, nilai))

    conn.commit()
    cursor.close()
    return True

def reset_perbandingan_kriteria():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM perbandingan_kriteria")
    conn.commit()
    cursor.close()
    return True

def get_perbandingan_subkriteria(id_kriteria):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM perbandingan_subkriteria 
        WHERE id_kriteria = %s
    """, (id_kriteria,))
    rows = cursor.fetchall()
    cursor.close()
    return rows

def save_perbandingan_subkriteria(id_kriteria, id1, id2, nilai):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM perbandingan_subkriteria 
        WHERE id_kriteria = %s AND id_subkriteria1 = %s AND id_subkriteria2 = %s
    """, (id_kriteria, id1, id2))

    if cursor.fetchone():
        cursor.execute("""
            UPDATE perbandingan_subkriteria 
            SET nilai_perbandingan = %s 
            WHERE id_kriteria = %s AND id_subkriteria1 = %s AND id_subkriteria2 = %s
        """, (nilai, id_kriteria, id1, id2))
    else:
        cursor.execute("""
            INSERT INTO perbandingan_subkriteria 
            (id_kriteria, id_subkriteria1, id_subkriteria2, nilai_perbandingan)
            VALUES (%s, %s, %s, %s)
        """, (id_kriteria, id1, id2, nilai))

    conn.commit()
    cursor.close()
    return True

def reset_perbandingan_subkriteria(id_kriteria):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM perbandingan_subkriteria WHERE id_kriteria = %s", (id_kriteria,))
    conn.commit()
    cursor.close()
    return True

def get_subkriteria_weights():
    kriteria_list = get_all_kriteria()
    all_weights = {}      # {id_kriteria: {id_subkriteria: bobot}}
    cr_map = {}           # {id_kriteria: CR}

    for k in kriteria_list:
        id_kriteria = k["id_kriteria"]
        sub_list = get_subkriteria_by_kriteria(id_kriteria)
        id_map = {s['id_subkriteria']: s['nama_subkriteria'] for s in sub_list}
        id_list = list(id_map.keys())
        n = len(id_list)

        if n < 2:
            continue

        matrix = np.ones((n, n))
        nilai_map = {
            (row[1], row[2]): float(row[3])
            for row in get_perbandingan_subkriteria(id_kriteria)
        }

        for i in range(n):
            for j in range(n):
                if i != j:
                    matrix[i][j] = nilai_map.get((id_list[i], id_list[j]), 1.0)

        result = calculate_ahp(matrix)
        bobot = dict(zip(id_list, result["weights"]))
        all_weights[id_kriteria] = bobot
        cr_map[id_kriteria] = result["cr"]

    return all_weights, cr_map

def get_kriteria_weights():
    kriteria_list = get_all_kriteria()
    id_map = {k["id_kriteria"]: k["nama_kriteria"] for k in kriteria_list}
    id_list = list(id_map.keys())
    n = len(id_list)

    if n < 2:
        return {}, 0.0, 0.0

    matrix = np.ones((n, n))
    nilai_map = {
        (row[0], row[1]): float(row[2])
        for row in get_perbandingan_kriteria()
    }

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = nilai_map.get((id_list[i], id_list[j]), 1.0)

    result = calculate_ahp(matrix)
    weights = dict(zip(id_list, result["weights"]))

    return weights, result["cr"], result["ri"]

def calculate_total_scores():
    kriteria_weights, kriteria_cr, _ = get_kriteria_weights()
    subkriteria_weights, subkriteria_cr = get_subkriteria_weights()
    guru_list = get_all_guru()

    # Ambil semua nilai subkriteria
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_subkriteria")
    rows = cursor.fetchall()
    nilai_all = [dict(zip([col[0] for col in cursor.description], row)) for row in rows]
    cursor.close()

    results = []
    for guru in guru_list:
        total_score = 0
        detail = {}

        for id_kriteria, bobot_kriteria in kriteria_weights.items():
            sub_map = subkriteria_weights.get(id_kriteria, {})
            skor_kriteria = 0

            for id_sub, bobot_sub in sub_map.items():
                nilai = next((
                    n["nilai"] for n in nilai_all
                    if n["id_guru"] == guru["id_guru"] and n["id_subkriteria"] == id_sub
                ), 0)
                skor_kriteria += nilai * bobot_sub

            skor_kriteria_final = skor_kriteria * bobot_kriteria
            total_score += skor_kriteria_final
            detail[f"Kriteria {id_kriteria}"] = skor_kriteria_final

        results.append({
            "id_guru": guru["id_guru"],
            "nama_guru": guru["nama_guru"],
            "total_score": total_score,
            "detail_scores": detail
        })

    return results, kriteria_cr, subkriteria_cr