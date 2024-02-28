"""adding watchlist table

Revision ID: b2dbf5f00ab4
Revises: 6a2b56c355ed
Create Date: 2024-02-28 13:50:27.326963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2dbf5f00ab4'
down_revision = '6a2b56c355ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('watchlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('watchlist_stocks',
    sa.Column('watchlist_id', sa.Integer(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.ForeignKeyConstraint(['watchlist_id'], ['watchlist.id'], ),
    sa.PrimaryKeyConstraint('watchlist_id', 'stock_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watchlist_stocks')
    op.drop_table('watchlist')
    # ### end Alembic commands ###
