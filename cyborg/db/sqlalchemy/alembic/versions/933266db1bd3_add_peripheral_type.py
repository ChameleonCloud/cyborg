"""add_peripheral_type

Revision ID: 933266db1bd3
Revises: c1b5abada09c
Create Date: 2021-07-07 17:36:55.265337

"""

# revision identifiers, used by Alembic.
revision = '933266db1bd3'
down_revision = 'c1b5abada09c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    new_device_type = sa.Enum('GPU', 'FPGA', 'AICHIP', 'PERIPHERAL',
                              name='device_type')
    op.alter_column('devices', 'type',
                    existing_type=new_device_type,
                    nullable=False)
