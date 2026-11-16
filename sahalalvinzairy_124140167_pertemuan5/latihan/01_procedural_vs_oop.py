# Cara prosedural: data dan fungsi ditulis terpisah.
nama_buku = "Bumi"

def tampilkan_buku(nama):
    print("Buku:", nama)


tampilkan_buku(nama_buku)

# Cara OOP: data dan perilakunya disimpan dalam satu class.
class Buku:
    def __init__(self, nama):
        self.nama = nama

    def tampilkan(self):
        print("Object buku:", self.nama)


buku = Buku("Laskar Pelangi")
buku.tampilkan()
