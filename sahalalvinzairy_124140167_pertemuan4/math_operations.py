"""Kumpulan fungsi geometri dan konversi suhu."""

PI = 3.14159


def luas_persegi(sisi):
    """Menghitung luas persegi.

    Args:
        sisi: Panjang sisi persegi.
    Returns:
        Luas persegi.
    """
    return sisi * sisi


def keliling_persegi(sisi):
    """Menghitung keliling persegi.

    Args:
        sisi: Panjang sisi persegi.
    Returns:
        Keliling persegi.
    """
    return 4 * sisi


def luas_persegi_panjang(panjang, lebar):
    """Menghitung luas persegi panjang.

    Args:
        panjang: Panjang persegi panjang.
        lebar: Lebar persegi panjang.
    Returns:
        Luas persegi panjang.
    """
    return panjang * lebar


def keliling_persegi_panjang(panjang, lebar):
    """Menghitung keliling persegi panjang.

    Args:
        panjang: Panjang persegi panjang.
        lebar: Lebar persegi panjang.
    Returns:
        Keliling persegi panjang.
    """
    return 2 * (panjang + lebar)


def luas_lingkaran(jari_jari):
    """Menghitung luas lingkaran.

    Args:
        jari_jari: Panjang jari-jari lingkaran.
    Returns:
        Luas lingkaran.
    """
    return PI * jari_jari * jari_jari


def keliling_lingkaran(jari_jari):
    """Menghitung keliling lingkaran.

    Args:
        jari_jari: Panjang jari-jari lingkaran.
    Returns:
        Keliling lingkaran.
    """
    return 2 * PI * jari_jari


def celsius_ke_fahrenheit(suhu_celsius):
    """Mengubah suhu Celsius menjadi Fahrenheit.

    Args:
        suhu_celsius: Suhu dalam derajat Celsius.
    Returns:
        Suhu dalam derajat Fahrenheit.
    """
    return (suhu_celsius * 9 / 5) + 32


def celsius_ke_kelvin(suhu_celsius):
    """Mengubah suhu Celsius menjadi Kelvin.

    Args:
        suhu_celsius: Suhu dalam derajat Celsius.
    Returns:
        Suhu dalam Kelvin.
    """
    return suhu_celsius + 273.15
