"""Add product SKU, reorder level, and updated timestamp."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# Revision identifiers
revision: str = "381752d32151"
down_revision: str | Sequence[str] | None = "fea6ac2aa3b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add SKU as nullable first to support existing products.
    op.add_column(
        "products",
        sa.Column("sku", sa.String(length=50), nullable=True),
    )

    # Assign a unique SKU to every existing product.
    op.execute("UPDATE products SET sku = CONCAT('SKU-', product_id) WHERE sku IS NULL")

    # Make SKU required and unique after backfilling.
    op.alter_column(
        "products",
        "sku",
        existing_type=sa.String(length=50),
        nullable=False,
    )
    op.create_unique_constraint(
        "uq_products_sku",
        "products",
        ["sku"],
    )

    # Add the remaining fields.
    op.add_column(
        "products",
        sa.Column(
            "reorder_level",
            sa.Integer(),
            server_default="10",
            nullable=False,
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("products", "updated_at")
    op.drop_column("products", "reorder_level")
    op.drop_constraint(
        "uq_products_sku",
        "products",
        type_="unique",
    )
    op.drop_column("products", "sku")
