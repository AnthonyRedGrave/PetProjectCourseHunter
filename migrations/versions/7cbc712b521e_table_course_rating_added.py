"""table course rating added

Revision ID: 7cbc712b521e
Revises: 3a59b9e0f873
Create Date: 2022-11-04 13:06:03.243725

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

RATINGS_STATUSES = [
        ("incr", "1"),
        ("decr", "-1")
]


# revision identifiers, used by Alembic.
revision = '7cbc712b521e'
down_revision = '3a59b9e0f873'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course_ratings', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('course_ratings', sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(choices=RATINGS_STATUSES), nullable=True))
    op.create_foreign_key(None, 'course_ratings', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'course_ratings', type_='foreignkey')
    op.drop_column('course_ratings', 'status')
    op.drop_column('course_ratings', 'user_id')
    # ### end Alembic commands ###
