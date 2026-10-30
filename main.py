# Sistem Reservasi Tiket Bioskop
# Tahap 1 - Array of Struct (list of dict)

daftar_reservasi = []

def garis():
    print("=" * 105)

def format_tanggal_valid(tanggal):
    bagian = tanggal.split("-")
    return (tanggal.count("-") == 2 and len(bagian) == 3
            and len(bagian[0]) == 4 and len(bagian[1]) == 2
            and len(bagian[2]) == 2 and all(x.isdigit() for x in bagian))

def tampilkan_tabel(data):
    if not data:
        print("Belum ada data reservasi yang tersimpan.")
        return
    garis()
    print(f"{'No':<4}{'Kode':<12}{'Nama Pemesan':<20}{'Film':<22}{'Tanggal':<13}"
          f"{'Jam':<8}{'Studio':<9}{'Tiket':<7}{'Kursi':<12}{'Status':<14}")
    garis()
    for i, r in enumerate(data, 1):
        print(f"{i:<4}{r['kode_reservasi']:<12}{r['nama_pemesan'][:19]:<20}"
              f"{r['detail'][:21]:<22}{r['tanggal']:<13}{r['jam_tayang']:<8}"
              f"{r['studio']:<9}{r['jumlah_tiket']:<7}{r['nomor_kursi']:<12}"
              f"{r['status']:<14}")
    garis()
    print(f"Jumlah data: {len(data)}")

def tambah_reservasi():
    print("\n--- TAMBAH RESERVASI TIKET ---")
    kode = input("Kode reservasi: ").strip()
    if not kode:
        print("Kode reservasi tidak boleh kosong."); return
    if len(kode) < 3:
        print("Kode reservasi minimal 3 karakter."); return
    if any(r["kode_reservasi"].lower() == kode.lower() for r in daftar_reservasi):
        print("Kode reservasi sudah digunakan."); return

    nama = input("Nama pemesan: ").strip()
    if not nama:
        print("Nama pemesan tidak boleh kosong."); return

    jenis = input("Jenis reservasi (Tiket): ").strip().capitalize()
    if jenis != "Tiket":
        print("Untuk sistem ini, jenis reservasi harus Tiket."); return

    film = input("Judul film: ").strip()
    if not film:
        print("Judul film tidak boleh kosong."); return

    tanggal = input("Tanggal menonton (YYYY-MM-DD): ").strip()
    if not format_tanggal_valid(tanggal):
        print("Format tanggal salah. Gunakan format YYYY-MM-DD, contoh: 2026-10-15.")
        return

    jam = input("Jam tayang (contoh 19:30): ").strip()
    if len(jam) != 5 or jam[2] != ":" or not (jam[:2].isdigit() and jam[3:].isdigit()):
        print("Format jam tayang harus HH:MM, contoh 19:30."); return

    studio = input("Studio: ").strip()
    if not studio:
        print("Studio tidak boleh kosong."); return

    try:
        jumlah = int(input("Jumlah tiket: ").strip())
        if jumlah < 1:
            print("Jumlah tiket minimal 1."); return
    except ValueError:
        print("Jumlah tiket harus berupa angka."); return

    kursi = input("Nomor kursi (pisahkan dengan koma jika lebih dari satu): ").strip()
    daftar_kursi = [k.strip().upper() for k in kursi.split(",") if k.strip()]
    if len(daftar_kursi) != jumlah:
        print("Jumlah nomor kursi harus sama dengan jumlah tiket."); return
    if len(set(daftar_kursi)) != len(daftar_kursi):
        print("Nomor kursi tidak boleh duplikat."); return

    for r in daftar_reservasi:
        if (r["tanggal"] == tanggal and r["jam_tayang"] == jam
                and r["studio"].lower() == studio.lower()
                and r["status"] == "Aktif"
                and set(daftar_kursi).intersection(r["nomor_kursi"].split(", "))):
            print("Salah satu kursi sudah dipesan pada jadwal tersebut."); return

    reservasi = {
        "kode_reservasi": kode, "nama_pemesan": nama, "jenis": "Tiket",
        "detail": film, "tanggal": tanggal, "status": "Aktif",
        "jam_tayang": jam, "studio": studio, "jumlah_tiket": jumlah,
        "nomor_kursi": ", ".join(daftar_kursi)
    }
    daftar_reservasi.append(reservasi)
    print(f"Reservasi {kode} atas nama {nama} berhasil ditambahkan.")

def cari_reservasi():
    print("\n1. Cari berdasarkan kode\n2. Cari berdasarkan nama pemesan")
    mode = input("Pilih mode pencarian: ").strip()
    kata = input("Masukkan kata kunci: ").strip()
    if not kata:
        print("Kata kunci tidak boleh kosong."); return
    if mode == "1":
        hasil = [r for r in daftar_reservasi if r["kode_reservasi"].lower() == kata.lower()]
    elif mode == "2":
        hasil = [r for r in daftar_reservasi if kata.lower() in r["nama_pemesan"].lower()]
    else:
        print("Pilihan pencarian tidak valid."); return
    if hasil:
        tampilkan_tabel(hasil)
    else:
        jenis = "kode" if mode == "1" else "nama pemesan"
        print(f"Reservasi dengan {jenis} '{kata}' tidak ditemukan.")

def update_status():
    kode = input("Masukkan kode reservasi: ").strip()
    data = next((r for r in daftar_reservasi if r["kode_reservasi"].lower() == kode.lower()), None)
    if data is None:
        print(f"Reservasi dengan kode '{kode}' tidak ditemukan."); return
    if data["status"] in ("Selesai", "Dibatalkan"):
        print("Status reservasi ini sudah final dan tidak bisa diubah lagi."); return
    status_baru = input("Status baru (Selesai/Dibatalkan): ").strip().capitalize()
    if status_baru not in ("Selesai", "Dibatalkan"):
        print("Status tidak valid. Pilih Selesai atau Dibatalkan."); return
    lama = data["status"]
    data["status"] = status_baru
    print(f"Status reservasi {kode} atas nama {data['nama_pemesan']} berhasil diperbarui: "
          f"{lama} menjadi {status_baru}.")

def filter_status():
    status = input("Pilih status (Aktif/Selesai/Dibatalkan): ").strip().capitalize()
    if status not in ("Aktif", "Selesai", "Dibatalkan"):
        print("Pilihan status tidak valid."); return
    hasil = [r for r in daftar_reservasi if r["status"] == status]
    if hasil:
        print(f"Menampilkan reservasi dengan status: {status} ({len(hasil)} data)")
        tampilkan_tabel(hasil)
    else:
        print(f"Tidak ada reservasi dengan status '{status}'.")

def hapus_reservasi():
    kode = input("Masukkan kode reservasi yang akan dihapus: ").strip()
    indeks = next((i for i, r in enumerate(daftar_reservasi)
                   if r["kode_reservasi"].lower() == kode.lower()), None)
    if indeks is None:
        print(f"Reservasi dengan kode '{kode}' tidak ditemukan."); return
    r = daftar_reservasi[indeks]
    print("\nDetail reservasi:")
    print(f"Nama: {r['nama_pemesan']} | Film: {r['detail']} | Tanggal: {r['tanggal']}")
    print(f"Jam: {r['jam_tayang']} | Studio: {r['studio']} | Kursi: {r['nomor_kursi']}")
    konfirmasi = input("Yakin menghapus reservasi ini? (y/n): ").strip().lower()
    if konfirmasi == "y":
        daftar_reservasi.pop(indeks)
        print(f"Reservasi {kode} atas nama {r['nama_pemesan']} berhasil dihapus dari sistem.")
    else:
        print("Penghapusan dibatalkan.")

def menu_utama():
    while True:
        print("\n")
        garis()
        print("              SISTEM RESERVASI TIKET BIOSKOP")
        garis()
        print("1. Tambah Reservasi Baru")
        print("2. Tampilkan Semua Reservasi")
        print("3. Cari Reservasi")
        print("4. Update Status Reservasi")
        print("5. Filter Reservasi Berdasarkan Status")
        print("6. Hapus Reservasi")
        print("0. Keluar")
        garis()
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1": tambah_reservasi()
        elif pilihan == "2": tampilkan_tabel(daftar_reservasi)
        elif pilihan == "3": cari_reservasi()
        elif pilihan == "4": update_status()
        elif pilihan == "5": filter_status()
        elif pilihan == "6": hapus_reservasi()
        elif pilihan == "0":
            print("Terima kasih telah menggunakan Sistem Reservasi Tiket Bioskop.")
            break
        else:
            print("Menu tidak tersedia. Silakan pilih kembali.")

if __name__ == "__main__":
    menu_utama()
