"""empty message

Revision ID: 01b6d8c099f0
Revises: 42a7e106e644
Create Date: 2023-11-09 09:27:51.163207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01b6d8c099f0'
down_revision = '42a7e106e644'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eyes_color', sa.String(length=80), nullable=True))
        batch_op.drop_column('eye_color')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eye_color', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
        batch_op.drop_column('eyes_color')

    # ### end Alembic commands ###
