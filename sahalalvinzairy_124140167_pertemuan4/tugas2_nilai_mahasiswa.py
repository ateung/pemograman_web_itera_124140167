"""Menghitung nilai akhir dan grade beberapa mahasiswa."""

mahasiswa = [
    {
        "nama": "Andi Saputra",
        "nim": "124140101",
        "nilai_uts": 80,
        "nilai_uas": 90,
        "nilai_tugas": 85,
    },
    {
        "nama": "Bunga Lestari",
        "nim": "124140102",
        "nilai_uts": 70,
        "nilai_uas": 75,
        "nilai_tugas": 80,
    },
    {
        "nama": "Citra Dewi",
        "nim": "124140103",
        "nilai_uts": 60,
        "nilai_uas": 65,
        "nilai_tugas": 70,
    },
    {
        "nama": "Dimas Pratama",
        "nim": "124140104",
        "nilai_uts": 45,
        "nilai_uas": 55,
        "nilai_tugas": 60,
    },
    {
        "nama": "Eka Putri",
        "nim": "124140105",
        "nilai_uts": 30,
        "nilai_uas": 40,
        "nilai_tugas": 45,
    },
]


def hitung_nilai_akhir(data):
    """Menghitung nilai akhir seorang mahasiswa.

    Args:
        data: Dictionary berisi nilai UTS, UAS, dan tugas.
    Returns:
        Nilai akhir berdasarkan bobot penilaian.
    """
    nilai_uts = data["nilai_uts"]
    nilai_uas = data["nilai_uas"]
    nilai_tugas = data["nilai_tugas"]
    return (0.30 * nilai_uts) + (0.40 * nilai_uas) + (0.30 * nilai_tugas)


def tentukan_grade(nilai_akhir):
    """Menentukan grade dari nilai akhir.

    Args:
        nilai_akhir: Nilai akhir mahasiswa.
    Returns:
        Huruf grade dari A sampai E.
    """
    if nilai_akhir >= 80:
        return "A"
    elif nilai_akhir >= 70:
        return "B"
    elif nilai_akhir >= 60:
        return "C"
    elif nilai_akhir >= 50:
        return "D"
    else:
        return "E"


def tampilkan_tabel(daftar_mahasiswa):
    """Mencetak data mahasiswa dalam bentuk tabel.

    Args:
        daftar_mahasiswa: List dictionary data mahasiswa.
    Returns:
        Tidak mengembalikan nilai; tabel dicetak ke terminal.
    """
    print(f"{'Nama':<20} {'NIM':<12} {'Nilai Akhir':>12} {'Grade':>7}")
    print("-" * 55)

    for data in daftar_mahasiswa:
        nilai_akhir = hitung_nilai_akhir(data)
        grade = tentukan_grade(nilai_akhir)
        print(
            f"{data['nama']:<20} {data['nim']:<12} "
            f"{nilai_akhir:>12.2f} {grade:>7}"
        )


def main():
    """Menampilkan tabel serta nilai tertinggi dan terendah.

    Tidak menerima parameter dan tidak mengembalikan nilai.
    """
    print("=== DAFTAR NILAI MAHASISWA ===")
    tampilkan_tabel(mahasiswa)

    nilai_tertinggi = max(mahasiswa, key=hitung_nilai_akhir)
    nilai_terendah = min(mahasiswa, key=hitung_nilai_akhir)

    print("\nNilai tertinggi:")
    print(
        f"{nilai_tertinggi['nama']} - "
        f"{hitung_nilai_akhir(nilai_tertinggi):.2f} "
        f"(Grade {tentukan_grade(hitung_nilai_akhir(nilai_tertinggi))})"
    )
    print("Nilai terendah:")
    print(
        f"{nilai_terendah['nama']} - "
        f"{hitung_nilai_akhir(nilai_terendah):.2f} "
        f"(Grade {tentukan_grade(hitung_nilai_akhir(nilai_terendah))})"
    )


if __name__ == "__main__":
    main()
