"""user social links

Revision ID: 6745f805e273
Revises: 656849addbcf
Create Date: 2023-02-24 20:56:38.241775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6745f805e273'
down_revision = '656849addbcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('facebook', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('twitter', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('instagram', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('linkedin', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('snapchat', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('reddit', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('mastodon', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('tiktok', sa.String(length=64), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_facebook'), ['facebook'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_instagram'), ['instagram'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_linkedin'), ['linkedin'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_mastodon'), ['mastodon'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_reddit'), ['reddit'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_snapchat'), ['snapchat'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_tiktok'), ['tiktok'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_twitter'), ['twitter'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_twitter'))
        batch_op.drop_index(batch_op.f('ix_user_tiktok'))
        batch_op.drop_index(batch_op.f('ix_user_snapchat'))
        batch_op.drop_index(batch_op.f('ix_user_reddit'))
        batch_op.drop_index(batch_op.f('ix_user_mastodon'))
        batch_op.drop_index(batch_op.f('ix_user_linkedin'))
        batch_op.drop_index(batch_op.f('ix_user_instagram'))
        batch_op.drop_index(batch_op.f('ix_user_facebook'))
        batch_op.drop_column('tiktok')
        batch_op.drop_column('mastodon')
        batch_op.drop_column('reddit')
        batch_op.drop_column('snapchat')
        batch_op.drop_column('linkedin')
        batch_op.drop_column('instagram')
        batch_op.drop_column('twitter')
        batch_op.drop_column('facebook')

    # ### end Alembic commands ###
