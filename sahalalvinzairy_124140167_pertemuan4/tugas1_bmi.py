"""Program sederhana untuk menghitung BMI."""


def hitung_bmi(berat_kg, tinggi_meter):
    """Menghitung BMI dari berat dan tinggi badan.

    Args:
        berat_kg: Berat badan dalam kilogram.
        tinggi_meter: Tinggi badan dalam meter.
    Returns:
        Nilai BMI sebagai angka desimal.
    """
    return berat_kg / (tinggi_meter * tinggi_meter)


def tentukan_kategori(bmi):
    """Menentukan kategori berat badan.

    Args:
        bmi: Nilai BMI yang sudah dihitung.
    Returns:
        Nama kategori BMI.
    """
    if bmi < 18.5:
        return "Berat badan kurang"
    elif bmi < 25:
        return "Berat badan normal"
    elif bmi < 30:
        return "Berat badan berlebih"
    else:
        return "Obesitas"


def main():
    """Meminta data pengguna dan menampilkan hasil BMI.

    Tidak menerima parameter dan tidak mengembalikan nilai.
    """
    print("=== PENGHITUNG BMI ===")

    try:
        berat_kg = float(input("Masukkan berat badan (kg): "))
        tinggi_meter = float(input("Masukkan tinggi badan (meter): "))
    except ValueError:
        print("Input harus berupa angka.")
        return

    if berat_kg <= 0 or tinggi_meter <= 0:
        print("Berat dan tinggi harus lebih dari 0.")
        return

    bmi = hitung_bmi(berat_kg, tinggi_meter)
    kategori = tentukan_kategori(bmi)

    print(f"\nNilai BMI : {bmi:.2f}")
    print(f"Kategori  : {kategori}")


if __name__ == "__main__":
    main()
