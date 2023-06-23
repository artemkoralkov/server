"""create rooms table

Revision ID: 9b0f7a11cdd7
Revises: 
Create Date: 2023-04-05 14:40:11.867297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b0f7a11cdd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rooms',
        sa.Column('id', sa.String, primary_key=True, index=True),
        sa.Column('number', sa.Integer, index=True),
        sa.Column('building_number', sa.Integer, default=1),
        sa.Column('floor', sa.Integer),
        sa.Column('with_computers', sa.Boolean, default=False),
        sa.Column('with_projector', sa.Boolean, default=False),
        sa.Column('max_people', sa.Integer),
    )


def downgrade() -> None:
    op.drop_table('rooms')
    op.drop_table('rooms_reservation')
    # op.drop_table('lessons')
