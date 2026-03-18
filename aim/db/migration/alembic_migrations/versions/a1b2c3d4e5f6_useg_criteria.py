# Copyright (c) 2026 Cisco Systems
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Tables for uSeg microsegmentation criteria
Revision ID: a1b2c3d4e5f6
Revises: e322787e56fd
Create date: 2026-03-16 00:00:00.000000000
"""

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'e322787e56fd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'aim_endpoint_group_criteria',
        sa.Column('aim_id', sa.String(64), nullable=False),
        sa.Column('tenant_name', sa.String(64), nullable=False),
        sa.Column('app_profile_name', sa.String(64), nullable=False),
        sa.Column('epg_name', sa.String(64), nullable=False),
        sa.Column('display_name', sa.String(256), nullable=False, default=''),
        sa.Column('match', sa.String(16)),
        sa.Column('monitored', sa.Boolean, nullable=False, default=False),
        sa.Column('epoch', sa.BigInteger(), nullable=False,
                  server_default='0'),
        sa.PrimaryKeyConstraint('aim_id'),
        sa.UniqueConstraint('tenant_name', 'app_profile_name', 'epg_name',
                            name='uniq_aim_endpoint_group_criteria_identity'),
        sa.Index('idx_aim_endpoint_group_criteria_identity',
                 'tenant_name', 'app_profile_name', 'epg_name'))

    op.create_table(
        'aim_endpoint_group_ip_attr',
        sa.Column('aim_id', sa.String(64), nullable=False),
        sa.Column('tenant_name', sa.String(64), nullable=False),
        sa.Column('app_profile_name', sa.String(64), nullable=False),
        sa.Column('epg_name', sa.String(64), nullable=False),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('display_name', sa.String(256), nullable=False, default=''),
        sa.Column('ip', sa.String(64), nullable=False, default=''),
        sa.Column('use_subnet', sa.Boolean, nullable=False, default=False),
        sa.Column('monitored', sa.Boolean, nullable=False, default=False),
        sa.Column('epoch', sa.BigInteger(), nullable=False,
                  server_default='0'),
        sa.PrimaryKeyConstraint('aim_id'),
        sa.UniqueConstraint('tenant_name', 'app_profile_name', 'epg_name',
                            'name',
                            name='uniq_aim_endpoint_group_ip_attr_identity'),
        sa.Index('idx_aim_endpoint_group_ip_attr_identity',
                 'tenant_name', 'app_profile_name', 'epg_name', 'name'))

    op.create_table(
        'aim_endpoint_group_mac_attr',
        sa.Column('aim_id', sa.String(64), nullable=False),
        sa.Column('tenant_name', sa.String(64), nullable=False),
        sa.Column('app_profile_name', sa.String(64), nullable=False),
        sa.Column('epg_name', sa.String(64), nullable=False),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('display_name', sa.String(256), nullable=False, default=''),
        sa.Column('mac', sa.String(24), nullable=False, default=''),
        sa.Column('monitored', sa.Boolean, nullable=False, default=False),
        sa.Column('epoch', sa.BigInteger(), nullable=False,
                  server_default='0'),
        sa.PrimaryKeyConstraint('aim_id'),
        sa.UniqueConstraint('tenant_name', 'app_profile_name', 'epg_name',
                            'name',
                            name='uniq_aim_endpoint_group_mac_attr_identity'),
        sa.Index('idx_aim_endpoint_group_mac_attr_identity',
                 'tenant_name', 'app_profile_name', 'epg_name', 'name'))

    op.create_table(
        'aim_endpoint_group_vm_attr',
        sa.Column('aim_id', sa.String(64), nullable=False),
        sa.Column('tenant_name', sa.String(64), nullable=False),
        sa.Column('app_profile_name', sa.String(64), nullable=False),
        sa.Column('epg_name', sa.String(64), nullable=False),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('display_name', sa.String(256), nullable=False, default=''),
        sa.Column('type', sa.String(32), nullable=False, default='vm-name'),
        sa.Column('operator', sa.String(16), nullable=False,
                  default='equals'),
        sa.Column('value', sa.String(512), nullable=False, default=''),
        sa.Column('monitored', sa.Boolean, nullable=False, default=False),
        sa.Column('epoch', sa.BigInteger(), nullable=False,
                  server_default='0'),
        sa.PrimaryKeyConstraint('aim_id'),
        sa.UniqueConstraint('tenant_name', 'app_profile_name', 'epg_name',
                            'name',
                            name='uniq_aim_endpoint_group_vm_attr_identity'),
        sa.Index('idx_aim_endpoint_group_vm_attr_identity',
                 'tenant_name', 'app_profile_name', 'epg_name', 'name'))


def downgrade():
    pass
