"""add content column to posts table

Revision ID: a931dff76b6e
Revises: 9da7f659ae4e
Create Date: 2023-06-21 16:39:09.598574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a931dff76b6e'
down_revision = '9da7f659ae4e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
