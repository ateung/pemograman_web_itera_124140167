"""Membuat tabel dan mengisi data contoh untuk kedua resource API."""

import argparse
from datetime import date

from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from ..models import Base, Mahasiswa, Matakuliah


def setup_models(dbsession):
    """Menambahkan data awal jika tabel masih kosong."""
    if dbsession.query(Mahasiswa).count() == 0:
        dbsession.add_all(
            [
                Mahasiswa(
                    nim="12345",
                    nama="Budi Santoso",
                    jurusan="Teknik Informatika",
                    tanggal_lahir=date(2000, 5, 15),
                    alamat="Jl. Merdeka No. 123, Bandung",
                ),
                Mahasiswa(
                    nim="54321",
                    nama="Siti Aminah",
                    jurusan="Sistem Informasi",
                    tanggal_lahir=date(2001, 8, 22),
                    alamat="Jl. Mawar No. 45, Jakarta",
                ),
            ]
        )

    if dbsession.query(Matakuliah).count() == 0:
        dbsession.add_all(
            [
                Matakuliah(
                    kode_mk="IF2110", nama_mk="Pemrograman Web", sks=3, semester=3
                ),
                Matakuliah(kode_mk="IF3140", nama_mk="Basis Data", sks=3, semester=4),
                Matakuliah(
                    kode_mk="IF2210",
                    nama_mk="Pemrograman Berorientasi Objek",
                    sks=3,
                    semester=3,
                ),
            ]
        )
    dbsession.commit()


def main(argv=None):
    """Menjalankan pembuatan tabel dan seeding dari file INI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config_uri", help="File konfigurasi, misalnya development.ini"
    )
    args = parser.parse_args(argv)

    setup_logging(args.config_uri)
    settings = get_appsettings(args.config_uri)
    engine = engine_from_config(settings, prefix="sqlalchemy.")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        setup_models(session)
        print("Tabel siap dan data awal berhasil diperiksa.")
    finally:
        session.close()
        engine.dispose()


if __name__ == "__main__":
    main()
