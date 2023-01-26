"""add attribution and licence to dataset

Revision ID: 6985980cdcbf
Revises: c549883b9eb4
Create Date: 2023-01-26 12:47:55.888391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6985980cdcbf"
down_revision = "c549883b9eb4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("dataset", schema=None) as batch_op:
        batch_op.add_column(sa.Column("attribution", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("licence", sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("dataset", schema=None) as batch_op:
        batch_op.drop_column("licence")
        batch_op.drop_column("attribution")

    # ### end Alembic commands ###
