from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config

from ..models import Matakuliah


REQUIRED_FIELDS = ("kode_mk", "nama_mk", "sks", "semester")


def _read_json(request):
    """Membaca body JSON atau menghasilkan respons 400 jika tidak valid."""
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


def _validate_fields(data, required=False):
    """Memeriksa field teks dan angka agar tidak kosong atau bernilai negatif."""
    if required:
        for field in REQUIRED_FIELDS:
            if field not in data or data[field] is None or data[field] == "":
                return f"Field {field} wajib diisi."

    for field in ("kode_mk", "nama_mk"):
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return f"Field {field} harus berupa teks dan tidak boleh kosong."
            data[field] = data[field].strip()

    for field in ("sks", "semester"):
        if field in data:
            value = data[field]
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                return f"Field {field} harus berupa bilangan bulat lebih dari 0."

    return None


def _find_item(request, item_id):
    """Mencari matakuliah berdasarkan primary key."""
    try:
        numeric_id = int(item_id)
    except (TypeError, ValueError):
        return None
    return request.dbsession.query(Matakuliah).filter_by(id=numeric_id).first()


@view_config(route_name="matakuliah_list", request_method="GET", renderer="json")
def matakuliah_list(request):
    """Mengembalikan seluruh data matakuliah."""
    items = request.dbsession.query(Matakuliah).order_by(Matakuliah.id.asc()).all()
    return {"matakuliahs": [item.to_dict() for item in items]}


@view_config(route_name="matakuliah_detail", request_method="GET", renderer="json")
def matakuliah_detail(request):
    """Mengembalikan detail satu matakuliah."""
    item = _find_item(request, request.matchdict["id"])
    if item is None:
        return HTTPNotFound(
            json_body={"error": "Matakuliah tidak ditemukan."}
        )
    return {"matakuliah": item.to_dict()}


@view_config(route_name="matakuliah_add", request_method="POST", renderer="json")
def matakuliah_add(request):
    """Memvalidasi dan menyimpan matakuliah baru."""
    data, error_response = _read_json(request)
    if error_response:
        return error_response

    error_message = _validate_fields(data, required=True)
    if error_message:
        return HTTPBadRequest(json_body={"error": error_message})

    session = request.dbsession
    duplicate = session.query(Matakuliah).filter_by(kode_mk=data["kode_mk"]).first()
    if duplicate:
        return HTTPBadRequest(json_body={"error": "kode_mk sudah digunakan."})

    item = Matakuliah(**{field: data[field] for field in REQUIRED_FIELDS})
    session.add(item)
    session.flush()
    return {"success": True, "matakuliah": item.to_dict()}


@view_config(route_name="matakuliah_update", request_method="PUT", renderer="json")
def matakuliah_update(request):
    """Memperbarui field matakuliah yang dikirim."""
    item = _find_item(request, request.matchdict["id"])
    if item is None:
        return HTTPNotFound(
            json_body={"error": "Matakuliah tidak ditemukan."}
        )

    data, error_response = _read_json(request)
    if error_response:
        return error_response
    if not data:
        return HTTPBadRequest(json_body={"error": "Body JSON tidak boleh kosong."})

    error_message = _validate_fields(data)
    if error_message:
        return HTTPBadRequest(json_body={"error": error_message})

    if "kode_mk" in data:
        duplicate = (
            request.dbsession.query(Matakuliah)
            .filter(Matakuliah.kode_mk == data["kode_mk"], Matakuliah.id != item.id)
            .first()
        )
        if duplicate:
            return HTTPBadRequest(json_body={"error": "kode_mk sudah digunakan."})

    for field in REQUIRED_FIELDS:
        if field in data:
            setattr(item, field, data[field])

    return {"success": True, "matakuliah": item.to_dict()}


@view_config(
    route_name="matakuliah_delete", request_method="DELETE", renderer="json"
)
def matakuliah_delete(request):
    """Menghapus matakuliah berdasarkan ID."""
    item = _find_item(request, request.matchdict["id"])
    if item is None:
        return HTTPNotFound(
            json_body={"error": "Matakuliah tidak ditemukan."}
        )

    request.dbsession.delete(item)
    return {"success": True, "message": "Matakuliah berhasil dihapus."}
