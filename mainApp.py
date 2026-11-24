import customtkinter as ctk
import database

# Konfigurasi aplikasi
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Lumina Notes")
app.geometry("700x600")
app.configure(fg_color="#141326")

# Header aplikasi
header = ctk.CTkFrame(
    app,
    fg_color="#514A9B",
    corner_radius=0,
    height=65
)

header.pack(fill="x")
header.pack_propagate(False)

# Judul aplikasi
app_title = ctk.CTkLabel(
    header,
    text="Lumina Notes",
    font=("Arial", 22, "bold"),
    text_color="#F1E9DD"
)

app_title.pack(side="left", padx=20)



# Area catatan
notes_container = ctk.CTkScrollableFrame(
    app,
    fg_color="transparent",
    width=450,
    height=450
)

notes_container.pack(
    padx=15,
    pady=15,
    fill="both",
    expand=True
)


# Function membuat catatan
def tambah_catatan():

    note = ctk.CTkFrame(
        notes_container,
        fg_color="#514A9B",
        corner_radius=15
    )

    note.pack(fill="x", padx=10, pady=10)

    title = ctk.CTkEntry(
        note,
        placeholder_text="Judul catatan...",
        fg_color="#141326",
        text_color="#F1E9DD",
        border_width=0
    )

    title.pack(fill="x", padx=15, pady=(15, 5))

    content = ctk.CTkTextbox(
        note,
        height=100,
        fg_color="#141326",
        text_color="#F1E9DD",
        corner_radius=10
    )

    content.pack(fill="x", padx=15, pady=10)

    # Function menyimpan catatan
    def simpan_catatan():
        judul = title.get().strip()
        isi = content.get("1.0", "end-1c")

        if not judul:
            title.configure(placeholder_text="Judul wajib diisi!")
            return

        database.tambah_data(judul, isi)

        note.destroy()
        tampilkan_catatan()

    # Tombol simpan
    save_button = ctk.CTkButton(
        note,
        text="Simpan",
        fg_color="#30252A",
        hover_color="#756DBA",
        command=simpan_catatan
    )

    save_button.pack(pady=(0, 15))


# Function menampilkan catatan
def tampilkan_catatan():

    # Menghapus tampilan catatan sebelumnya
    for widget in notes_container.winfo_children():
        widget.destroy()

    # Mengambil data dari database
    data = database.ambil_data()
    print(data)

    for id_note, judul, isi in data:

        note = ctk.CTkFrame(
            notes_container,
            fg_color="#514A9B",
            corner_radius=12,
            border_width=1,
            border_color="#514A9B"
        )

        note.pack(fill="x", padx=10, pady=8)

        # Judul catatan
        title = ctk.CTkLabel(
            note,
            text=judul,
            text_color="#F1E9DD",
            font=("Arial", 18, "bold"),
            anchor="w"
        )

        title.pack(fill="x", padx=20, pady=(15, 5))

        # Deskripsi catatan
        content = ctk.CTkLabel(
            note,
            text=isi,
            text_color="#B8AEB0",
            font=("Arial", 13),
            wraplength=850,
            anchor="w",
            justify="left"
        )

        content.pack(fill="x", padx=20, pady=(0, 15))

        # Area tombol
        button_frame = ctk.CTkFrame(
            note,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 12)
        )

        # Tombol hapus
        delete_button = ctk.CTkButton(
            button_frame,
            text="Hapus",
            width=70,
            height=28,
            fg_color="#69434B",
            hover_color="#8D555F",
            corner_radius=8,
            command=lambda id_note=id_note: hapus_catatan(id_note)
        )

        delete_button.pack(side="right", padx=(5, 5))

        # Tombol edit
        edit_button = ctk.CTkButton(
            button_frame,
            text="Edit",
            width=70,
            height=28,
            fg_color="#514A9B",
            hover_color="#756DBA",
            corner_radius=8,
            command=lambda id_note=id_note, judul=judul, isi=isi: edit_catatan(id_note, judul, isi)
        )

        edit_button.pack(side="right", padx=5)

def hapus_catatan(id_note):
    database.hapus_data(id_note)
    tampilkan_catatan()

def edit_catatan(id_note, judul_lama, isi_lama):

    # Membuat jendela edit
    edit_window = ctk.CTkToplevel(app)
    edit_window.title("Edit Catatan")
    edit_window.geometry("350x400")
    edit_window.configure(fg_color="#141326")

    # Input judul
    title_entry = ctk.CTkEntry(
        edit_window,
        placeholder_text="Judul catatan...",
        fg_color="#30252A",
        text_color="#F1E9DD"
    )

    title_entry.pack(fill="x", padx=20, pady=(20, 10))

    title_entry.insert(0, judul_lama)

    # Input isi
    content_entry = ctk.CTkTextbox(
        edit_window,
        height=200,
        fg_color="#30252A",
        text_color="#F1E9DD"
    )

    content_entry.pack(fill="both", padx=20, pady=10)

    content_entry.insert("1.0", isi_lama)

    # Function menyimpan perubahan
    def simpan_edit():

        judul_baru = title_entry.get().strip()
        isi_baru = content_entry.get("1.0", "end-1c")

        if not judul_baru:
            return

        database.ubah_data(id_note, judul_baru, isi_baru)

        edit_window.destroy()
        tampilkan_catatan()

    # Tombol simpan
    save_button = ctk.CTkButton(
        edit_window,
        text="Simpan Perubahan",
        fg_color="#514A9B",
        hover_color="#756DBA",
        command=simpan_edit
    )

    save_button.pack(pady=10)





# Tombol tambah catatan
# Area tombol tambah
add_button = ctk.CTkButton(
    header,
    text="+ Tambah Catatan",
    width=150,
    height=38,
    fg_color="#756DBA",
    hover_color="#433B85",
    text_color="#F1E9DD",
    corner_radius=10,
    command=tambah_catatan
)

add_button.pack(side="right", padx=15)

# Menampilkan data saat aplikasi dibuka
tampilkan_catatan()

app.mainloop()