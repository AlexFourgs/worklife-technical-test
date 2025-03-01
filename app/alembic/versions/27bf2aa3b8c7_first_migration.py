"""First migration

Revision ID: 27bf2aa3b8c7
Revises: 
Create Date: 2022-05-19 15:22:57.500725

"""

from alembic import op
import sqlalchemy as sa

from app.model.base import CustomUUID

# revision identifiers, used by Alembic.
revision = "27bf2aa3b8c7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "employee",
        sa.Column("id", CustomUUID(as_uuid=True), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_employee_id"), "employee", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_employee_id"), table_name="employee")
    op.drop_table("employee")
    # ### end Alembic commands ###
