"""users table

Revision ID: 26d9a6ce825f
Revises: 
Create Date: 2023-02-21 13:42:17.995738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26d9a6ce825f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('section', sa.String(length=64), nullable=True),
    sa.Column('inguestlist', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_firstname'), ['firstname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_inguestlist'), ['inguestlist'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_lastname'), ['lastname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_role'), ['role'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_section'), ['section'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_section'))
        batch_op.drop_index(batch_op.f('ix_user_role'))
        batch_op.drop_index(batch_op.f('ix_user_lastname'))
        batch_op.drop_index(batch_op.f('ix_user_inguestlist'))
        batch_op.drop_index(batch_op.f('ix_user_firstname'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###