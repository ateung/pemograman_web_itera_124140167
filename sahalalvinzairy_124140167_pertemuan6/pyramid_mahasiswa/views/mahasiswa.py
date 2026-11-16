from datetime import date

from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import or_

from ..models import Mahasiswa


FIELDS = ("nim", "nama", "jurusan", "tanggal_lahir", "alamat")


def _read_json(request):
    """Membaca body JSON dan memastikan bentuknya object."""
    try:
        data = request.json_body
    except (ValueError, TypeError):
        return None, HTTPBadRequest(
            json_body={"error": "Body harus berupa JSON valid."}
        )
    if not isinstance(data, dict):
        return None, HTTPBadRequest(
            json_body={"error": "Body JSON harus berupa object."}
        )
    return data, None


def _validate(data, required=False):
    """Memeriksa field wajib, teks, dan tanggal lahir."""
    if required:
        for field in ("nim", "nama", "jurusan"):
            is_missing = field not in data
            is_invalid = not is_missing and (
                not isinstance(data[field], str) or not data[field].strip()
            )
            if is_missing or is_invalid:
                return f"Field {field} wajib diisi."

    for field in ("nim", "nama", "jurusan"):
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return f"Field {field} harus berupa teks dan tidak boleh kosong."
            data[field] = data[field].strip()

    if "tanggal_lahir" in data and data["tanggal_lahir"]:
        try:
            data["tanggal_lahir"] = date.fromisoformat(data["tanggal_lahir"])
        except (TypeError, ValueError):
            return "tanggal_lahir harus memakai format YYYY-MM-DD."
    elif "tanggal_lahir" in data:
        data["tanggal_lahir"] = None

    alamat_tidak_valid = (
        "alamat" in data
        and data["alamat"] is not None
        and not isinstance(data["alamat"], str)
    )
    if alamat_tidak_valid:
        return "Field alamat harus berupa teks."
    return None


def _find_item(request, mahasiswa_id):
    """Mencari mahasiswa berdasarkan ID integer."""
    try:
        mahasiswa_id = int(mahasiswa_id)
    except (TypeError, ValueError):
        return None
    return request.dbsession.query(Mahasiswa).filter_by(id=mahasiswa_id).first()


@view_config(route_name="mahasiswa_list", request_method="GET", renderer="json")
def mahasiswa_list(request):
    """Mengembalikan daftar mahasiswa dan mendukung pencarian sederhana."""
    query = request.dbsession.query(Mahasiswa)
    search = request.params.get("q", "").strip()
    if search:
        query = query.filter(
            or_(Mahasiswa.nama.ilike(f"%{search}%"), Mahasiswa.nim.ilike(f"%{search}%"))
        )
    items = query.order_by(Mahasiswa.id.asc()).all()
    return {"mahasiswas": [item.to_dict() for item in items]}


@view_config(route_name="mahasiswa_detail", request_method="GET", renderer="json")
def mahasiswa_detail(request):
    """Mengembalikan detail satu mahasiswa."""
    item = _find_item(request, request.matchdict["id"])
    if item is None:
        return HTTPNotFound(json_body={"error": "Mahasiswa tidak ditemukan."})
    return {"mahasiswa": item.to_dict()}


@view_config(route_name="mahasiswa_add", request_method="POST", renderer="json")
def mahasiswa_add(request):
    """Memvalidasi dan menambahkan mahasiswa baru."""
    data, error_response = _read_json(request)
    if error_response:
        return error_response
    error_message = _validate(data, required=True)
    if error_message:
        return HTTPBadRequest(json_body={"error": error_message})

    session = request.dbsession
    if session.query(Mahasiswa).filter_by(nim=data["nim"]).first():
        return HTTPBadRequest(json_body={"error": "NIM sudah digunakan."})

    item = Mahasiswa(**{field: data.get(field) for field in FIELDS})
    session.add(item)
    session.flush()
    return {"success": True, "mahasiswa": item.to_dict()}


@view_config(route_name="mahasiswa_update", request_method="PUT", renderer="json")
def mahasiswa_update(request):
    """Memperbarui data mahasiswa sesuai field yang dikirim."""
    item = _find_item(request, request.matchdict["id"])
    if item is None:
        return HTTPNotFound(json_body={"error": "Mahasiswa tidak ditemukan."})

    data, error_response = _read_json(request)
    if error_response:
        return error_response
    if not data:
        return HTTPBadRequest(json_body={"error": "Body JSON tidak boleh kosong."})

    error_message = _validate(data)
    if error_message:
        return HTTPBadRequest(json_body={"error": error_message})

    if "nim" in data:
        duplicate = (
            request.dbsession.query(Mahasiswa)
            .filter(Mahasiswa.nim == data["nim"], Mahasiswa.id != item.id)
            .first()
        )
        if duplicate:
            return HTTPBadRequest(json_body={"error": "NIM sudah digunakan."})

    for field in FIELDS:
        if field in data:
            setattr(item, field, data[field])
    return {"success": True, "mahasiswa": item.to_dict()}


@view_config(route_name="mahasiswa_delete", request_method="DELETE", renderer="json")
def mahasiswa_delete(request):
    """Menghapus mahasiswa berdasarkan ID."""
    item = _find_item(request, request.matchdict["id"])
    if item is None:
        return HTTPNotFound(json_body={"error": "Mahasiswa tidak ditemukan."})
    request.dbsession.delete(item)
    return {"success": True, "message": "Mahasiswa berhasil dihapus."}
