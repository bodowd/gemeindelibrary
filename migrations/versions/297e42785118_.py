"""empty message

Revision ID: 297e42785118
Revises: 
Create Date: 2020-01-31 22:24:13.561882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '297e42785118'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reminder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('backup_title', sa.String(length=100), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=False),
    sa.Column('borrower', sa.String(length=100), nullable=True),
    sa.Column('borrower_email', sa.String(length=120), nullable=True),
    sa.Column('date_borrowed', sa.Date(), nullable=True),
    sa.Column('date_due', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book_list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_status')
    op.drop_table('test_table')
    op.drop_table('reminder')
    op.drop_table('book_list')
    # ### end Alembic commands ###
