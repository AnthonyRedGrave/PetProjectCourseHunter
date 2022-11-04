"""added language choice type

Revision ID: 3a59b9e0f873
Revises: 85c994faabb5
Create Date: 2022-11-03 12:58:39.361026

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

LANGUAGES = [("english", "english"), ("russian", "russian")]


# revision identifiers, used by Alembic.
revision = '3a59b9e0f873'
down_revision = '85c994faabb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('language', sqlalchemy_utils.types.choice.ChoiceType(choices=LANGUAGES), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'language')
    # ### end Alembic commands ###