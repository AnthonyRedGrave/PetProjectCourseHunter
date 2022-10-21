"""add difficult

Revision ID: 52fb7660efff
Revises: a0c91a989600
Create Date: 2022-10-19 18:59:19.277755

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


DIFFICULTES = [
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard')
]


# revision identifiers, used by Alembic.
revision = '52fb7660efff'
down_revision = 'a0c91a989600'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('difficult', sqlalchemy_utils.types.choice.ChoiceType(choices=DIFFICULTES), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'difficult')
    # ### end Alembic commands ###
