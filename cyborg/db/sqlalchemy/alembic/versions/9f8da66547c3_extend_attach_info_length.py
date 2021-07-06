"""extend_attach_info_length

Revision ID: 9f8da66547c3
Revises: 8e7a919df6ae
Create Date: 2021-07-14 16:51:37.945814

"""

# revision identifiers, used by Alembic.
revision = '9f8da66547c3'
down_revision = '8e7a919df6ae'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('attach_handles', 'attach_info',
                    existing_type=sa.Text(),
                    nullable=False)
