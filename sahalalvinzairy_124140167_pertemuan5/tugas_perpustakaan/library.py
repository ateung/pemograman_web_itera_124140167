from library_item import LibraryItem


class Library:
    """Menyimpan item dan menyediakan fitur katalog serta pencarian."""

    def __init__(self, name):
        self.name = name
        self.__koleksi = []

    @property
    def jumlah_item(self):
        """Jumlah seluruh item yang disimpan di perpustakaan."""
        return len(self.__koleksi)

    def add_item(self, item):
        """Menambahkan item jika tipe dan ID-nya belum digunakan."""
        if not isinstance(item, LibraryItem):
            return False

        for koleksi_item in self.__koleksi:
            if koleksi_item.item_id == item.item_id:
                return False

        self.__koleksi.append(item)
        return True

    def show_available_items(self):
        """Menampilkan katalog item yang sedang tersedia."""
        item_tersedia = [item for item in self.__koleksi if item.is_available]
        if not item_tersedia:
            print("Belum ada item yang tersedia.")
            return

        for item in item_tersedia:
            # Pemanggilan get_detail yang berbeda menunjukkan polymorphism.
            print(f"- {item.item_id}: {item.get_detail()}")

    def search_item(self, keyword):
        """Mencari item berdasarkan ID atau sebagian judul."""
        keyword = keyword.strip().lower()
        hasil = []
        for item in self.__koleksi:
            if keyword in item.item_id.lower() or keyword in item.title.lower():
                hasil.append(item)
        return hasil
