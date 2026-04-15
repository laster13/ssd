"""finalize backend migration chain

Revision ID: b8f4a0c7f5b1
Revises: 4c40fca6f315
Create Date: 2026-04-07 11:30:00.000000
"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "b8f4a0c7f5b1"
down_revision: Union[str, Sequence[str], None] = "4c40fca6f315"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass