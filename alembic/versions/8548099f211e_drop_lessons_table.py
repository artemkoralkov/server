"""drop lessons table

Revision ID: 8548099f211e
Revises: 9b0f7a11cdd7
Create Date: 2023-04-14 11:04:09.337220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8548099f211e'
down_revision = '9b0f7a11cdd7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    op.drop_table('lessons')
