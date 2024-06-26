"""empty message

Revision ID: 9a832c6659f8
Revises:
Create Date: 2024-03-11 09:52:28.899817

"""
from alembic import op
import sqlalchemy as sa
import os

# revision identifiers, used by Alembic.
revision = '9a832c6659f8'
down_revision = None
branch_labels = None
depends_on = None

environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

def upgrade():
    if environment == 'production' and SCHEMA:
        op.execute(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}')

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('user_about', sa.Text(), nullable=True),
    sa.Column('profile_pic', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    schema=SCHEMA if environment == 'production' else None
    )

    op.create_table('articles',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=True),
    sa.Column('article_url', sa.String(length=255), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('published_utc', sa.DateTime(), nullable=True),
    sa.Column('publisher', sa.JSON(), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema=SCHEMA if environment == 'production' else None
    )

    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('market_cap', sa.Float(), nullable=False),
    sa.Column('pe_ratio', sa.Float(), nullable=False),
    sa.Column('sector', sa.String(length=50), nullable=False),
    sa.Column('previous_close', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol'),
    schema=SCHEMA if environment == 'production' else None
    )

    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.String(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], [f'{SCHEMA}.articles.id'] if environment == 'production' else ['articles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], [f'{SCHEMA}.users.id'] if environment == 'production' else ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=SCHEMA if environment == 'production' else None
    )

    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], [f'{SCHEMA}.stocks.id'] if environment == 'production' else ['stocks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], [f'{SCHEMA}.users.id'] if environment == 'production' else ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=SCHEMA if environment == 'production' else None
    )

    op.create_table('pinned',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.String(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], [f'{SCHEMA}.articles.id'] if environment == 'production' else ['articles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], [f'{SCHEMA}.users.id'] if environment == 'production' else ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=SCHEMA if environment == 'production' else None
    )

    op.create_table('planner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], [f'{SCHEMA}.users.id'] if environment == 'production' else ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=SCHEMA if environment == 'production' else None
    )

    op.create_table('watchlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['stock_id'], [f'{SCHEMA}.stocks.id'] if environment == 'production' else ['stocks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], [f'{SCHEMA}.users.id'] if environment == 'production' else ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema=SCHEMA if environment == 'production' else None
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if environment == 'production' and SCHEMA:
        op.execute(f'DROP SCHEMA IF EXISTS {SCHEMA} CASCADE')

    op.drop_table('watchlist', schema=SCHEMA if environment == 'production' else None)
    op.drop_table('planner', schema=SCHEMA if environment == 'production' else None)
    op.drop_table('pinned', schema=SCHEMA if environment == 'production' else None)
    op.drop_table('notes', schema=SCHEMA if environment == 'production' else None)
    op.drop_table('comments', schema=SCHEMA if environment == 'production' else None)
    op.drop_table('stocks', schema=SCHEMA if environment == 'production' else None)
    op.drop_table('articles', schema=SCHEMA if environment == 'production' else None)
    op.drop_table('users', schema=SCHEMA if environment == 'production' else None)
    # ### end Alembic commands ###
