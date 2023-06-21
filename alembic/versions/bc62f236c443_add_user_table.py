"""Add user table

Revision ID: bc62f236c443
Revises: a931dff76b6e
Create Date: 2023-06-21 16:43:40.661581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc62f236c443'
down_revision = 'a931dff76b6e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')        
        )
    pass


def downgrade():
    op.drop_table('users')
    pass
