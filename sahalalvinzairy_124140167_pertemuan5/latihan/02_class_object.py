class Mahasiswa:
    """Contoh class dan object sederhana."""

    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim

    def perkenalan(self):
        print(f"Nama saya {self.nama}, NIM {self.nim}.")


mahasiswa1 = Mahasiswa("Sahal", "124140167")
mahasiswa1.perkenalan()
