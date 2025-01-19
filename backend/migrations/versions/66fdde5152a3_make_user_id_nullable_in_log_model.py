"""Make user_id nullable in Log model

Revision ID: 66fdde5152a3
Revises: 5351d9d34116
Create Date: 2025-01-10 04:04:44.696918

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "66fdde5152a3"
down_revision = "5351d9d34116"  # Replace this with the correct parent revision ID
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the desired schema
    op.create_table(
        "logs_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("action", sa.String, nullable=True),
        sa.Column("user_id", sa.Integer, nullable=True),  # Now nullable
        sa.Column("timestamp", sa.DateTime, nullable=False),
        sa.Column("module", sa.String, nullable=True),
        sa.Column("level", sa.String, nullable=True),
        sa.Column("meta_data", sa.JSON, nullable=True),
    )

    # Copy data from the old table to the new table
    op.execute(
        "INSERT INTO logs_temp (id, action, user_id, timestamp, module, level, meta_data) "
        "SELECT id, action, user_id, timestamp, module, level, meta_data FROM logs"
    )

    # Drop the old table
    op.drop_table("logs")

    # Rename the new table to replace the old one
    op.rename_table("logs_temp", "logs")


def downgrade():
    # Reverse the steps in downgrade
    op.create_table(
        "logs_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("action", sa.String, nullable=True),
        sa.Column("user_id", sa.Integer, nullable=False),  # Revert to NOT NULL
        sa.Column("timestamp", sa.DateTime, nullable=False),
        sa.Column("module", sa.String, nullable=True),
        sa.Column("level", sa.String, nullable=True),
        sa.Column("meta_data", sa.JSON, nullable=True),
    )

    # Copy data back to the old schema
    op.execute(
        "INSERT INTO logs_temp (id, action, user_id, timestamp, module, level, meta_data) "
        "SELECT id, action, user_id, timestamp, module, level, meta_data FROM logs"
    )

    # Drop the current table
    op.drop_table("logs")

    # Rename the temporary table back to logs
    op.rename_table("logs_temp", "logs")
