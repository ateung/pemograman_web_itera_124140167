from library import Library
from library_item import Book, Magazine
from member import Member


def tampilkan_hasil_pencarian(library, keyword):
    """Mencetak hasil pencarian berdasarkan judul atau ID."""
    print(f"\nPencarian: {keyword}")
    hasil = library.search_item(keyword)
    if not hasil:
        print("Item tidak ditemukan.")
        return

    for item in hasil:
        print(f"- {item.item_id}: {item.get_detail()}")


def main():
    """Menjalankan contoh fitur sistem perpustakaan."""
    library = Library("Pojok Baca ITERA")
    anggota = Member("A001", "Sahal")

    library.add_item(Book("B001", "Laskar Pelangi", 2005, "Andrea Hirata"))
    library.add_item(Book("B002", "Bumi", 2014, "Tere Liye"))
    library.add_item(Magazine("M001", "Teknologi Hari Ini", 2025, "Edisi 12"))

    print("=" * 54)
    print(f"KATALOG {library.name.upper()}")
    print("=" * 54)
    print(f"Jumlah item: {library.jumlah_item}")
    print("\nDaftar item yang tersedia:")
    library.show_available_items()

    tampilkan_hasil_pencarian(library, "laskar")
    tampilkan_hasil_pencarian(library, "M001")

    item = library.search_item("B001")[0]
    print(f"\nPeminjaman oleh {anggota.name}: {item.title}")
    item.borrow()
    print(f"Status setelah dipinjam: {'Tersedia' if item.is_available else 'Dipinjam'}")

    print("\nKatalog setelah peminjaman:")
    library.show_available_items()

    print("\nMenambahkan item baru:")
    item_baru = Magazine("M002", "Sains Mingguan", 2026, "Edisi 4")
    if library.add_item(item_baru):
        print(f"Item {item_baru.item_id} berhasil ditambahkan.")
    print(f"Jumlah item sekarang: {library.jumlah_item}")
    library.show_available_items()


if __name__ == "__main__":
    main()
