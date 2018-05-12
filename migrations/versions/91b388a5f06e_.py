"""empty message

Revision ID: 91b388a5f06e
Revises: 447081da9629
Create Date: 2018-05-12 08:49:14.669012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91b388a5f06e'
down_revision = '447081da9629'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_meals')
    op.add_column('orders', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('orders', sa.Column('menu_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'orders', ['date'])
    op.create_foreign_key(None, 'orders', 'menus', ['menu_id'], ['menu_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'orders', type_='unique')
    op.drop_column('orders', 'menu_id')
    op.drop_column('orders', 'date')
    op.create_table('order_meals',
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('meal_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['meal_id'], ['meals.meal_id'], name='order_meals_meal_id_fkey'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], name='order_meals_order_id_fkey'),
    sa.PrimaryKeyConstraint('order_id', 'meal_id', name='order_meals_pkey')
    )
    # ### end Alembic commands ###
