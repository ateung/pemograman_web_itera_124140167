from setuptools import find_packages, setup


setup(
    name="pyramid-mahasiswa",
    version="0.1.0",
    description="REST API sederhana untuk data mahasiswa dan matakuliah",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "alembic>=1.13",
        "psycopg2-binary>=2.9",
        "pyramid>=2.0",
        "pyramid-tm>=2.5",
        "sqlalchemy>=2.0",
        "transaction>=4.0",
        "waitress>=3.0",
        "zope.sqlalchemy>=3.1",
    ],
    extras_require={"testing": ["pytest>=8.0", "WebTest>=3.0"]},
    entry_points={
        "paste.app_factory": ["main = pyramid_mahasiswa:main"],
    },
)
