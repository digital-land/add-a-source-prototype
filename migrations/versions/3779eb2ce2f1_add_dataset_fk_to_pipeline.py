"""add dataset fk to pipeline

Revision ID: 3779eb2ce2f1
Revises: e2387ced9b81
Create Date: 2023-02-28 15:06:05.250067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3779eb2ce2f1"
down_revision = "e2387ced9b81"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pipeline", schema=None) as batch_op:
        batch_op.add_column(sa.Column("dataset_id", sa.Text(), nullable=False))
        batch_op.create_foreign_key(
            "pipeline_dataset_id_fkey", "dataset", ["dataset_id"], ["dataset"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pipeline", schema=None) as batch_op:
        batch_op.drop_constraint("pipeline_dataset_id_fkey", type_="foreignkey")
        batch_op.drop_column("dataset_id")

    # ### end Alembic commands ###