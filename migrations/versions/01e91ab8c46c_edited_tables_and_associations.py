"""Edited tables and associations

Revision ID: 01e91ab8c46c
Revises: 94091340be1d
Create Date: 2024-02-28 15:13:47.345479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e91ab8c46c'
down_revision = '94091340be1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
