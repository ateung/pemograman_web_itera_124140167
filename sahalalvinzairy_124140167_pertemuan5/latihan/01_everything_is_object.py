# Di Python, nilai seperti angka dan teks adalah object.
angka = 10
teks = "Belajar Python"

print("Nilai:", angka, "| Tipe:", type(angka).__name__)
print("Nilai:", teks, "| Tipe:", type(teks).__name__)
print("Apakah angka termasuk int?", isinstance(angka, int))
