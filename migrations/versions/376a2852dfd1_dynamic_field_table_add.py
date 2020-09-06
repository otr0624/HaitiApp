"""Dynamic field table add

Revision ID: 376a2852dfd1
Revises: 890b136e6a13
Create Date: 2020-07-29 09:00:38.523442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '376a2852dfd1'
down_revision = '890b136e6a13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pp_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('duo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pp_set_id', sa.Integer(), nullable=True),
    sa.Column('patient_name', sa.String(length=100), nullable=True),
    sa.Column('provider_name', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pp_set_id'], ['pp_set.id'], ),
    sa.ForeignKeyConstraint(['provider_name'], ['provider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('duo')
    op.drop_table('pp_set')
    # ### end Alembic commands ###