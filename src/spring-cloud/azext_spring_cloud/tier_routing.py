# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=wrong-import-order
from ._enterprise import (app_get_enterprise, app_deploy_enterprise)
from .custom import (app_get, app_deploy)
from .vendored_sdks.appplatform.v2022_05_01_preview import AppPlatformManagementClient
from azure.cli.core.commands.client_factory import get_mgmt_service_client
from knack.log import get_logger

logger = get_logger(__name__)


def _get_client(cmd):
    return get_mgmt_service_client(cmd.cli_ctx, AppPlatformManagementClient)


def _is_enterprise_tier(client, resource_group, name):
    resource = client.services.get(resource_group, name)
    return resource.sku.name == 'E0'


def app_get_routing(cmd, client,
            resource_group,
            service, name):
    if _is_enterprise_tier(client, resource_group, service):
        return app_get_enterprise(cmd, _get_client(cmd), resource_group, service, name)
    else:
        return app_get(cmd, client, resource_group, service, name)


def app_deploy_routing(cmd, client, resource_group, service, name,
                       version=None,
                       deployment=None,
                       artifact_path=None,
                       target_module=None,
                       runtime_version=None,
                       jvm_options=None,
                       main_entry=None,
                       env=None,
                       config_file_patterns=None,
                       no_wait=False):
    if _is_enterprise_tier(client, resource_group, service):
        return app_deploy_enterprise(cmd, _get_client(cmd), resource_group, service, name,
                                     version, deployment, artifact_path, target_module, 
                                     jvm_options, env, config_file_patterns, no_wait)
    else:
        return app_deploy(cmd, client, resource_group, service, name,
                          version, deployment, artifact_path, target_module, runtime_version, 
                          jvm_options, main_entry, env, no_wait)