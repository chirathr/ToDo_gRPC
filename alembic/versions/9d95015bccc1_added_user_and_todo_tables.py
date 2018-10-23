"""Added User and ToDo tables

Revision ID: 9d95015bccc1
Revises: 
Create Date: 2018-10-23 14:57:48.031282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d95015bccc1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )

    op.create_table(
        'todo',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('text', sa.String),
        sa.Column('is_done', sa.Boolean, default=False),
        sa.Column('user_id', sa.Boolean, sa.ForeignKey('user.id'))
    )


def downgrade():
   op.drop_table('user')
   op.drop_table('todo')
