from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Kelas dasar untuk item yang dapat disimpan di perpustakaan."""

    def __init__(self, item_id, title, year):
        self._item_id = item_id
        self._title = title
        self._year = year
        self._is_borrowed = False

    @property
    def item_id(self):
        """Mengembalikan ID item."""
        return self._item_id

    @property
    def title(self):
        """Mengembalikan judul item."""
        return self._title

    @property
    def is_available(self):
        """Status tersedia bernilai True jika item belum dipinjam."""
        return not self._is_borrowed

    def borrow(self):
        """Mengubah status item menjadi dipinjam jika masih tersedia."""
        if self._is_borrowed:
            return False
        self._is_borrowed = True
        return True

    def return_item(self):
        """Mengubah status item menjadi tersedia kembali."""
        if not self._is_borrowed:
            return False
        self._is_borrowed = False
        return True

    @abstractmethod
    def get_detail(self):
        """Mengembalikan informasi item dalam bentuk teks."""
        raise NotImplementedError


class Book(LibraryItem):
    """Item buku dengan informasi nama penulis."""

    def __init__(self, item_id, title, year, author):
        super().__init__(item_id, title, year)
        self._author = author

    def get_detail(self):
        """Menampilkan detail khusus buku."""
        status = "Tersedia" if self.is_available else "Dipinjam"
        return f"[Buku] {self.title} | Penulis: {self._author} | Tahun: {self._year} | {status}"


class Magazine(LibraryItem):
    """Item majalah dengan informasi nomor edisi."""

    def __init__(self, item_id, title, year, edition):
        super().__init__(item_id, title, year)
        self._edition = edition

    def get_detail(self):
        """Menampilkan detail khusus majalah."""
        status = "Tersedia" if self.is_available else "Dipinjam"
        return f"[Majalah] {self.title} | Edisi: {self._edition} | Tahun: {self._year} | {status}"
