class Member:
    """Menyimpan identitas sederhana anggota perpustakaan."""

    def __init__(self, member_id, name):
        self.__member_id = member_id
        self.__name = name

    @property
    def member_id(self):
        """Mengembalikan ID anggota."""
        return self.__member_id

    @property
    def name(self):
        """Mengembalikan nama anggota."""
        return self.__name
