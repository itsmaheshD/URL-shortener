"""allow nullable short code

Revision ID: 48a596b8003a
Revises: 78e40574df1a
Create Date: 2026-08-25 16:41:59.940498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48a596b8003a'
down_revision: Union[str, Sequence[str], None] = '78e40574df1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'urlrecord',
        'short_code_url',
        existing_type=sa.String(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'urlrecord',
        'short_code_url',
        existing_type=sa.String(),
        nullable=False,
    )
