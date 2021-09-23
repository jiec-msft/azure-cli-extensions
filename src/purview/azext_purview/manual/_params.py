# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements

from azure.cli.core.commands.parameters import (
    tags_type,
    get_enum_type,
    resource_group_name_type,
    get_location_type
)
from azure.cli.core.commands.validators import get_default_location_from_resource_group


def load_arguments(self, _):

    with self.argument_context('purview account create') as c:
        c.argument('resource_group_name', resource_group_name_type)
        c.argument('account_name', options_list=['--name', '-n', '--account-name'], type=str, help='The name of the '
                   'account.')
        c.argument('location', arg_type=get_location_type(self.cli_ctx), required=False,
                   validator=get_default_location_from_resource_group)
        c.argument('tags', tags_type)
        c.argument('managed_group_name', type=str, help='Gets or sets the managed resource group name')
        c.argument('public_network_access', arg_type=get_enum_type(['NotSpecified', 'Enabled', 'Disabled']),
                   help='Gets or sets the public network access.')

    with self.argument_context('purview account update') as c:
        c.argument('resource_group_name', resource_group_name_type)
        c.argument('account_name', options_list=['--name', '-n', '--account-name'], type=str, help='The name of the '
                   'account.', id_part='name')
        c.argument('tags', tags_type)
        c.argument('managed_group_name', type=str, help='Gets or sets the managed resource group name')
        c.argument('public_network_access', arg_type=get_enum_type(['NotSpecified', 'Enabled', 'Disabled']),
                   help='Gets or sets the public network access.')

    with self.argument_context('purview default-account set') as c:
        c.argument('account_name', options_list=['--name', '-n', '--account-name'], type=str,
                   help='The name of the account that is set as the default.')
        c.argument('resource_group_name', resource_group_name_type)
        c.argument('scope', type=str, help='The scope object ID. For example, sub ID or tenant ID.')
        c.argument('scope_tenant_id', type=str, help='The scope tenant in which the default account is set.')
        c.argument('scope_type', arg_type=get_enum_type(['Tenant', 'Subscription']), help='The scope where the default '
                   'account is set.')
        c.argument('subscription_id', type=str, help='The subscription ID of the account that is set as the default.')
