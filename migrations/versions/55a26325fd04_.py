"""empty message

Revision ID: 55a26325fd04
Revises: 9f0dc058f27b
Create Date: 2023-05-06 08:54:15.970032

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '55a26325fd04'
down_revision = '9f0dc058f27b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('img', sa.String(length=500), nullable=True))
    op.drop_column('user', 'mac_no')
    op.drop_column('user', 'image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('user', sa.Column('mac_no', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('user', 'img')
    # ### end Alembic commands ###
