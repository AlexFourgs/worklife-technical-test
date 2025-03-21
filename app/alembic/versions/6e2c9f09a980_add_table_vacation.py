"""add_table_vacation

Revision ID: 6e2c9f09a980
Revises: 186cfec3778f
Create Date: 2025-03-01 20:18:44.287248

"""

from alembic import op
import sqlalchemy as sa


from app.model.base import CustomUUID

# revision identifiers, used by Alembic.
revision = "6e2c9f09a980"
down_revision = "186cfec3778f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vacation",
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("employee_id", CustomUUID(), nullable=True),
        sa.Column("id", CustomUUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employee.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vacation_id"), "vacation", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_vacation_id"), table_name="vacation")
    op.drop_table("vacation")
    # ### end Alembic commands ###
