from datetime import date

import pytest
from pyramid_mahasiswa import main
from pyramid_mahasiswa.models import Base, Mahasiswa, Matakuliah
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from webtest import TestApp


@pytest.fixture
def client(tmp_path):
    """Membuat aplikasi dan database SQLite baru untuk setiap test."""
    database_path = tmp_path / "test.sqlite"
    database_url = f"sqlite:///{database_path.as_posix()}"
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    session.add_all(
        [
            Mahasiswa(
                nim="12345",
                nama="Budi Santoso",
                jurusan="Teknik Informatika",
                tanggal_lahir=date(2000, 5, 15),
                alamat="Bandung",
            ),
            Matakuliah(
                kode_mk="IF2110",
                nama_mk="Pemrograman Web",
                sks=3,
                semester=3,
            ),
        ]
    )
    session.commit()
    session.close()

    app = TestApp(main({}, **{"sqlalchemy.url": database_url}))
    yield app
    engine.dispose()


def test_matakuliah_crud_and_validation(client):
    """Menguji daftar, detail, tambah, ubah, hapus, dan validasi matakuliah."""
    response = client.get("/api/matakuliah")
    assert response.status_int == 200
    assert response.json["matakuliahs"][0]["kode_mk"] == "IF2110"

    detail = client.get("/api/matakuliah/1")
    assert detail.json["matakuliah"]["nama_mk"] == "Pemrograman Web"
    client.get("/api/matakuliah/999", status=404)

    client.post_json("/api/matakuliah", {"kode_mk": "IF3000"}, status=400)
    client.post_json(
        "/api/matakuliah",
        {
            "kode_mk": "IF3140",
            "nama_mk": "Basis Data",
            "sks": 3,
            "semester": 4,
        },
    )
    client.post_json(
        "/api/matakuliah",
        {
            "kode_mk": "IF3001",
            "nama_mk": "Nilai tidak valid",
            "sks": 0,
            "semester": 4,
        },
        status=400,
    )
    client.post_json(
        "/api/matakuliah",
        {
            "kode_mk": "IF3002",
            "nama_mk": "Semester tidak valid",
            "sks": 3,
            "semester": -1,
        },
        status=400,
    )
    client.post_json(
        "/api/matakuliah",
        {
            "kode_mk": "IF2110",
            "nama_mk": "Kode duplikat",
            "sks": 3,
            "semester": 3,
        },
        status=400,
    )

    updated = client.put_json(
        "/api/matakuliah/2", {"nama_mk": "Basis Data Lanjut"}
    )
    assert updated.json["matakuliah"]["nama_mk"] == "Basis Data Lanjut"
    client.put_json("/api/matakuliah/999", {"nama_mk": "Tidak ada"}, status=404)

    deleted = client.delete("/api/matakuliah/2")
    assert deleted.json["success"] is True
    client.delete("/api/matakuliah/2", status=404)


def test_mahasiswa_crud(client):
    """Menguji operasi dasar API mahasiswa."""
    response = client.get("/api/mahasiswa")
    assert response.json["mahasiswas"][0]["nim"] == "12345"
    assert len(client.get("/api/mahasiswa?q=Budi").json["mahasiswas"]) == 1
    client.get("/api/mahasiswa/999", status=404)

    created = client.post_json(
        "/api/mahasiswa",
        {"nim": "67890", "nama": "Ahmad Fadli", "jurusan": "Teknik Elektro"},
    )
    mahasiswa_id = created.json["mahasiswa"]["id"]
    updated = client.put_json(
        f"/api/mahasiswa/{mahasiswa_id}", {"jurusan": "Sistem Informasi"}
    )
    assert updated.json["mahasiswa"]["jurusan"] == "Sistem Informasi"
    client.delete(f"/api/mahasiswa/{mahasiswa_id}")
    client.get(f"/api/mahasiswa/{mahasiswa_id}", status=404)
