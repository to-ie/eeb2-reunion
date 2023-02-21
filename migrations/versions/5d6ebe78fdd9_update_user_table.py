"""update user table

Revision ID: 5d6ebe78fdd9
Revises: 6d0288bc2596
Create Date: 2023-02-21 21:42:30.358469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d6ebe78fdd9'
down_revision = '6d0288bc2596'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('section', schema=None) as batch_op:
        batch_op.drop_index('ix_section_section')
        batch_op.create_index(batch_op.f('ix_section_section'), ['section'], unique=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_role')
        batch_op.create_index(batch_op.f('ix_user_role'), ['role'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_role'))
        batch_op.create_index('ix_user_role', ['role'], unique=False)

    with op.batch_alter_table('section', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_section_section'))
        batch_op.create_index('ix_section_section', ['section'], unique=False)

    # ### end Alembic commands ###
