"""added all products to the db models and populated

Revision ID: d475837d79c1
Revises: c3108cee3cc7
Create Date: 2024-06-05 22:16:16.746505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd475837d79c1'
down_revision: Union[str, None] = 'c3108cee3cc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('allproducts',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('createdat', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updatedat', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('allproducts')
    # ### end Alembic commands ###