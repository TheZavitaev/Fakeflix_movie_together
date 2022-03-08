"""add default room status

Revision ID: 1aa5b911ca00
Revises: bdbc51160e3b
Create Date: 2022-03-06 17:59:45.692241

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '1aa5b911ca00'
down_revision = 'bdbc51160e3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'movie_together_room', ['id'])
    op.create_unique_constraint(None, 'movie_together_room_user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movie_together_room_user', type_='unique')
    op.drop_constraint(None, 'movie_together_room', type_='unique')
    # ### end Alembic commands ###
