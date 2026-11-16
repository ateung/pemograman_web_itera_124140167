from pyramid.view import view_config


@view_config(route_name="home", renderer="json")
def home(request):
    """Memberikan informasi singkat tentang API."""
    return {
        "aplikasi": "API Mahasiswa dan Matakuliah",
        "status": "berjalan",
        "endpoint": ["/api/mahasiswa", "/api/matakuliah"],
    }
