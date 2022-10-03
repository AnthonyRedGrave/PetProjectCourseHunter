"""change accounttype

Revision ID: de2303a9cf05
Revises: 91ecc47aa180
Create Date: 2022-09-28 12:01:33.068283

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'de2303a9cf05'
down_revision = '91ecc47aa180'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profiles', 'type',
               existing_type=postgresql.ENUM('standart', 'premium', name='accounttype'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('profiles', 'type',
               existing_type=postgresql.ENUM('standart', 'premium', name='accounttype'),
               nullable=True)
    # ### end Alembic commands ###
