"""empty message

Revision ID: 50fa98f8fc9b
Revises: 
Create Date: 2019-02-08 05:37:09.169451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50fa98f8fc9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurant', sa.Column('name', sa.String, nullable=False))
    op.add_column('menuitem', sa.Column('course', sa.String, nullable=False))
    op.add_column('menuitem', sa.Column('description', sa.String, nullable=False))
    op.add_column('menuitem', sa.Column('name', sa.String, nullable=False))
    op.add_column('menuitem', sa.Column('price', sa.String, nullable=False))
    op.add_column('menuitem', sa.Column('restaurant', sa.String, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurant', 'name')
    op.drop_column('menuitem', 'course')
    op.drop_column('menuitem', 'description')
    op.drop_column('menuitem', 'price')
    op.drop_column('menuitem', 'name')
    op.drop_column('menuitem', 'restaurant')
    # ### end Alembic commands ###
