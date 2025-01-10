from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '5a5c3de1e623'
down_revision = '66fdde5152a3'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the desired schema
    op.create_table(
        'logs_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=True),  # Make user_id nullable
        sa.Column('action', sa.String(255), nullable=False),  # Ensure NOT NULL
        sa.Column('timestamp', sa.DateTime, nullable=True),  # Adjust as needed
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Copy data from the old table to the new table
    op.execute("""
        INSERT INTO logs_new (id, user_id, action, timestamp)
        SELECT id, user_id, action, timestamp
        FROM logs
    """)

    # Drop the old table
    op.drop_table('logs')

    # Rename the new table to the old table's name
    op.rename_table('logs_new', 'logs')


def downgrade():
    # Create the old table
    op.create_table(
        'logs_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),  # Revert user_id to NOT NULL
        sa.Column('action', sa.String(255), nullable=True),  # Adjust as needed
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Copy data from the new table to the old table
    op.execute("""
        INSERT INTO logs_old (id, user_id, action, timestamp)
        SELECT id, user_id, action, timestamp
        FROM logs
    """)

    # Drop the new table
    op.drop_table('logs')

    # Rename the old table back to its original name
    op.rename_table('logs_old', 'logs')
