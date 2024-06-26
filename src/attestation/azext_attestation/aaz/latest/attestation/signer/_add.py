# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "attestation signer add",
)
class Add(AAZCommand):
    """Adds a new attestation policy certificate to the set of policy     management certificates.

    :example: Adds a new attestation policy certificate to the set of policy management certificates.
        az attestation signer add -n "myattestationprovider" -g "MyResourceGroup" --signer "eyAiYWxnIjoiUlMyNTYiLCAie..."
    """

    _aaz_info = {
        "version": "2022-08-01",
        "resources": [
            ["data-plane:microsoft.attestation", "/certificates:add", "2022-08-01"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group "Client"

        _args_schema = cls._args_schema
        _args_schema.provider_name = AAZStrArg(
            options=["--provider-name"],
            arg_group="Client",
            help="Name of the attestation provider.",
            required=True,
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            arg_group="Client",
            help="Name of resource group. You can configure the default group using `az configure --defaults group=<name>`",
            required=True,
        )

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.signer = AAZStrArg(
            options=["--signer"],
            help="The policy certificate to add. An RFC7519 JSON Web Token containing a claim named \"maa-policyCertificate\" whose value is an RFC7517 JSON Web Key which specifies a new key to update. The RFC7519 JWT must be signed with one of the existing signing certificates.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*",
            ),
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.PolicyCertificatesAdd(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class PolicyCertificatesAdd(AAZHttpOperation):
        CLIENT_TYPE = "AAZMicrosoftAttestationDataPlaneClient_attestation"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/certificates:add",
                **self.url_parameters
            )

        @property
        def method(self):
            return "POST"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2022-08-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args.signer,
                typ=AAZStrType,
                typ_kwargs={"flags": {"required": True}}
            )

            return self.serialize_content(_content_value)

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.token = AAZStrType()

            return cls._schema_on_200


class _AddHelper:
    """Helper class for Add"""


__all__ = ["Add"]
