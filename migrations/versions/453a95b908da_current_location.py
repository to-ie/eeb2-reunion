"""current location

Revision ID: 453a95b908da
Revises: b6fbe78d4090
Create Date: 2023-03-03 19:42:55.171307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '453a95b908da'
down_revision = 'b6fbe78d4090'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currentlocation', sa.String(length=64), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_currentlocation'), ['currentlocation'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_currentlocation'))
        batch_op.drop_column('currentlocation')

    # ### end Alembic commands ###
