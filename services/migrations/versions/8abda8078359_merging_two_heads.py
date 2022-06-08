"""merging two heads

Revision ID: 8abda8078359
Revises: 37dceca85ffe, 619b76ea95b5
Create Date: 2022-06-07 23:40:33.741684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8abda8078359'
down_revision = ('37dceca85ffe', '619b76ea95b5')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass