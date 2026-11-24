import sqlite3

def koneksi():
    db = sqlite3.connect("database/notes.db")
    return db


def buat_tabel():
    db = koneksi()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT
        )
    """)

    db.commit()
    db.close()

# CREATE
def tambah_data(judul, isi):
    db = koneksi()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (judul, isi)
    )

    db.commit()
    db.close()


# READ
def ambil_data():
    db = koneksi()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM notes")

    data = cursor.fetchall()

    db.close()

    return data

# UPDATE
def ubah_data(id_note, judul, isi):
    db = koneksi()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE notes
        SET title = ?, content = ?
        WHERE id = ?
    """, (judul, isi, id_note))

    db.commit()
    db.close()

# DELETE
def hapus_data(id_note):
    db = koneksi()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (id_note,)
    )

    db.commit()
    db.close()


buat_tabel()