# Copyright 2026 Cisco, Inc.
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
#

"""Add action column to security group rules

Revision ID: b7c4d9e21a08
Revises: a1b2c3d4e5f6

"""

# revision identifiers, used by Alembic.
revision = 'b7c4d9e21a08'
down_revision = 'a1b2c3d4e5f6'


from alembic import op
import sqlalchemy as sa


# NOTE: server_default is 'permit' because that is the fabric's own default for
# hostprotRule.action. AID pushes every modelled attribute on every sync, so
# any other default here would rewrite the action of every existing security
# group rule in the fabric the first time the agent runs after this migration.
def upgrade():

    for table in ('aim_security_group_rules',
                  'aim_system_security_group_rules'):
        op.add_column(
            table,
            sa.Column('action', sa.String(32), nullable=False,
                      server_default='permit')
        )


def downgrade():
    pass
