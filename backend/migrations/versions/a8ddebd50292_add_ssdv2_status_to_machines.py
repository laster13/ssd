"""add ssdv2 status to machines

Revision ID: a8ddebd50292
Revises: 31d28043277b
Create Date: 2026-04-03 08:56:37.433250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8ddebd50292'
down_revision: Union[str, Sequence[str], None] = '31d28043277b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'machines',
        sa.Column(
            'ssdv2_installed',
            sa.Boolean(),
            server_default=sa.text('false'),
            nullable=False,
        ),
    )
    op.add_column(
        'machines',
        sa.Column('ssdv2_checked_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('machines', 'ssdv2_checked_at')
    op.drop_column('machines', 'ssdv2_installed')