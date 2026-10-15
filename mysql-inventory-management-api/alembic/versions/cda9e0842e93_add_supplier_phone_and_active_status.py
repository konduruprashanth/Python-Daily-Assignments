"""Add supplier phone and active status."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# Revision identifiers
revision: str = "cda9e0842e93"
down_revision: str | Sequence[str] | None = "381752d32151"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add phone and is_active columns to suppliers."""

    op.add_column(
        "suppliers",
        sa.Column("phone", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "suppliers",
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Remove phone and is_active columns from suppliers."""

    op.drop_column("suppliers", "is_active")
    op.drop_column("suppliers", "phone")
