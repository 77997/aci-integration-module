# Copyright (c) 2016 Cisco Systems
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

from oslo_config import cfg
from oslo_db.sqlalchemy import enginefacade

from aim import aim_store


_CTX_MANAGER = None


def _get_context_manager():
    global _CTX_MANAGER

    if _CTX_MANAGER is None:
        # oslo.db 18.0.0 removed the legacy EngineFacade (and its
        # session.EngineFacade alias). Use the modern enginefacade context
        # manager instead; configure() reads the connection from the
        # [database] section of cfg.CONF, matching the old from_config().
        _CTX_MANAGER = enginefacade.transaction_context()
        _CTX_MANAGER.configure(sqlite_fk=True)

    return _CTX_MANAGER


def get_engine():
    """Helper method to grab engine."""
    return _get_context_manager().writer.get_engine()


def dispose():
    # Don't need to do anything if a context manager hasn't been created
    if _CTX_MANAGER is not None:
        get_engine().pool.dispose()


def get_session(expire_on_commit=True, use_slave=False):
    """Helper method to grab session."""
    ctx = _get_context_manager()
    maker = (ctx.reader if use_slave else ctx.writer).get_sessionmaker()
    return maker(expire_on_commit=expire_on_commit)


def get_store(expire_on_commit=True, use_slave=False):
    store = cfg.CONF.aim.aim_store
    if store == 'sql':
        db_session = get_session(expire_on_commit=expire_on_commit,
                                 use_slave=use_slave)
        return aim_store.SqlAlchemyStore(db_session)
    elif store == 'k8s':
        return aim_store.K8sStore(
            namespace=cfg.CONF.aim_k8s.k8s_namespace,
            config_file=cfg.CONF.aim_k8s.k8s_config_path,
            vmm_domain=cfg.CONF.aim_k8s.k8s_vmm_domain,
            vmm_controller=cfg.CONF.aim_k8s.k8s_controller)
