"""create matakuliah table

Revision ID: 9e36a750119a
Revises: 20261116a001
Create Date: 2026-11-16 23:06:23.278110
"""

from alembic import op
import sqlalchemy as sa


revision = "9e36a750119a"
down_revision = "20261116a001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "matakuliah",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("kode_mk", sa.Text(), nullable=False),
        sa.Column("nama_mk", sa.Text(), nullable=False),
        sa.Column("sks", sa.Integer(), nullable=False),
        sa.Column("semester", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("kode_mk"),
    )


def downgrade():
    op.drop_table("matakuliah")
