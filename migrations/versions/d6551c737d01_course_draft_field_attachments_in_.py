"""course draft field, attachments in lesson, category logo, course logo upload

Revision ID: d6551c737d01
Revises: 52fb7660efff
Create Date: 2022-10-21 09:53:41.827278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6551c737d01'
down_revision = '52fb7660efff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('logo', sa.String(length=300), nullable=True))
    op.add_column('courses', sa.Column('logo', sa.String(length=300), nullable=True))
    op.add_column('courses', sa.Column('draft', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'draft')
    op.drop_column('courses', 'logo')
    op.drop_column('categories', 'logo')
    # ### end Alembic commands ###
