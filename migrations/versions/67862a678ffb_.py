"""empty message

Revision ID: 67862a678ffb
Revises: 26bf0dc8012e
Create Date: 2018-05-26 14:59:18.284237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67862a678ffb'
down_revision = '26bf0dc8012e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('move', sa.Column('icon', sa.String(length=168), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('move', 'icon')
    # ### end Alembic commands ###
