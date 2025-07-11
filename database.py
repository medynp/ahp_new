import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",     # atau 127.0.0.1
        user="root",          # sesuaikan
        password="",          # sesuaikan
        database="ahp_app"  # nama database
    )

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id_user INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            nama_lengkap VARCHAR(100) NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        )
    """)
    ("""
        CREATE TABLE IF NOT EXISTS guru (
            id_guru INTEGER PRIMARY KEY AUTO_INCREMENT,
            nama_guru TEXT NOT NULL,
            jabatan TEXT
        )
    """)
    ("""
        CREATE TABLE IF NOT EXISTS kriteria (
            id_kriteria INT AUTO_INCREMENT PRIMARY KEY,
            nama_kriteria VARCHAR(100) NOT NULL,
            deskripsi TEXT
        );
    """
    )
    ("""
        CREATE TABLE IF NOT EXISTS subkriteria (
            id_subkriteria INT AUTO_INCREMENT PRIMARY KEY,
            id_kriteria INT NOT NULL,
            nama_subkriteria VARCHAR(100) NOT NULL,
            deskripsi TEXT,
            FOREIGN KEY (id_kriteria) REFERENCES kriteria(id_kriteria) ON DELETE CASCADE
        );
    """)
    ("""
        CREATE TABLE IF NOT EXISTS nilai_subkriteria (
            id_nilai INT AUTO_INCREMENT PRIMARY KEY,
            id_guru INT NOT NULL,
            id_subkriteria INT NOT NULL,
            nilai INT NOT NULL,
            tanggal_penilaian DATE,
            FOREIGN KEY (id_guru) REFERENCES guru(id_guru) ON DELETE CASCADE,
            FOREIGN KEY (id_subkriteria) REFERENCES subkriteria(id_subkriteria) ON DELETE CASCADE
        );
    """)
    ("""
        CREATE TABLE IF NOT EXISTS perbandingan_kriteria (
            id_kriteria1 INT NOT NULL,
            id_kriteria2 INT NOT NULL,
            nilai_perbandingan DECIMAL(5, 2) NOT NULL,
            PRIMARY KEY (id_kriteria1, id_kriteria2),
            FOREIGN KEY (id_kriteria1) REFERENCES kriteria(id_kriteria),
            FOREIGN KEY (id_kriteria2) REFERENCES kriteria(id_kriteria)
        );
    """)
    ("""
        CREATE TABLE IF NOT EXISTS perbandingan_subkriteria (
            id_kriteria INT NOT NULL,
            id_subkriteria1 INT NOT NULL,
            id_subkriteria2 INT NOT NULL,
            nilai_perbandingan DECIMAL(5, 2) NOT NULL,
            PRIMARY KEY (id_kriteria, id_subkriteria1, id_subkriteria2),
            FOREIGN KEY (id_kriteria) REFERENCES kriteria(id_kriteria),
            FOREIGN KEY (id_subkriteria1) REFERENCES subkriteria(id_subkriteria),
            FOREIGN KEY (id_subkriteria2) REFERENCES subkriteria(id_subkriteria)
        );
    """)
    conn.commit()
    conn.close()