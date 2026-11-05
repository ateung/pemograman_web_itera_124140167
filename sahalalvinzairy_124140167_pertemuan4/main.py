"""Contoh penggunaan fungsi dari math_operations."""

import math_operations
from math_operations import celsius_ke_fahrenheit, celsius_ke_kelvin


def main():
    """Menjalankan contoh geometri dan konversi suhu.

    Tidak menerima parameter dan tidak mengembalikan nilai.
    """
    sisi = 4
    panjang = 8
    lebar = 5
    jari_jari = 7
    suhu_celsius = 25

    print("=== PERHITUNGAN GEOMETRI ===")
    print(f"Persegi (sisi {sisi})")
    print(f"  Luas     : {math_operations.luas_persegi(sisi):.2f}")
    print(f"  Keliling : {math_operations.keliling_persegi(sisi):.2f}")

    print(f"\nPersegi panjang ({panjang} x {lebar})")
    luas = math_operations.luas_persegi_panjang(panjang, lebar)
    print(f"  Luas     : {luas:.2f}")
    print(
        f"  Keliling : "
        f"{math_operations.keliling_persegi_panjang(panjang, lebar):.2f}"
    )

    print(f"\nLingkaran (jari-jari {jari_jari})")
    print(f"  Luas     : {math_operations.luas_lingkaran(jari_jari):.2f}")
    print(f"  Keliling : {math_operations.keliling_lingkaran(jari_jari):.2f}")
    print(f"  Nilai PI : {math_operations.PI}")

    print("\n=== KONVERSI SUHU ===")
    print(
        f"{suhu_celsius} C = "
        f"{celsius_ke_fahrenheit(suhu_celsius):.2f} F"
    )
    print(f"{suhu_celsius} C = {celsius_ke_kelvin(suhu_celsius):.2f} K")


if __name__ == "__main__":
    main()
