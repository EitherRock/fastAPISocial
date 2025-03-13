"""add user table

Revision ID: c01013b05df6
Revises: 56954242c9e5
Create Date: 2025-03-12 18:47:09.397097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c01013b05df6'
down_revision: Union[str, None] = '56954242c9e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')          
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('users')
    pass
