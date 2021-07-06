"""add_oci_runtime_attach_type

Revision ID: 8e7a919df6ae
Revises: 933266db1bd3
Create Date: 2021-07-07 18:03:07.673379

"""

# revision identifiers, used by Alembic.
revision = '8e7a919df6ae'
down_revision = '933266db1bd3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    new_attach_type = sa.Enum('PCI', 'MDEV', 'OCI_RUNTIME', 'TEST_PCI',
                              name='attach_handle_attach_type')
    op.alter_column('attach_handles', 'attach_type',
                    existing_type=new_attach_type,
                    nullable=False)
