from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import zope.sqlalchemy

from .mahasiswa import Mahasiswa
from .matakuliah import Matakuliah
from .meta import Base


def get_engine(settings, prefix="sqlalchemy."):
    """Membuat engine database dari pengaturan aplikasi."""
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    """Membuat factory untuk session SQLAlchemy."""
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_tm_session(session_factory, transaction_manager):
    """Mendaftarkan session agar mengikuti transaksi setiap request."""
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """Menyiapkan koneksi database dan request.dbsession."""
    settings = config.get_settings()
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry["dbsession_factory"] = session_factory
    config.registry["dbengine"] = engine
    config.add_request_method(
        lambda request: get_tm_session(session_factory, request.tm),
        "dbsession",
        reify=True,
    )
