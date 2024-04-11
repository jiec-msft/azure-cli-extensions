# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

import json
import unittest

from azext_spring.jobs.job import (job_create, job_update, _update_args, _update_envs, _update_job_properties,
                                   _update_secrets,
                                   _is_job_execution_in_final_state)
from azext_spring.vendored_sdks.appplatform.v2024_05_01_preview.models import (EnvSecretsCollection, EnvVar,
                                                                               JobExecutionTemplate,
                                                                               JobResource,
                                                                               JobResourceProperties,
                                                                               Secret)

from .test_asa_job_utils import (sample_job_resource, sample_job_resource_after_update, expected_create_job_payload,
                                 expected_update_job_payload)
from ..common.test_utils import get_test_cmd

try:
    import unittest.mock as mock
except ImportError:
    from unittest import mock


class TestAsaJobs(unittest.TestCase):

    def setUp(self) -> None:
        self.envs_dict = {
            "prop1": "value1",
            "prop2": "value2"
        }
        self.secrets_dict = {
            "secret1": "secret_value1",
            "secret2": "secret_value2"
        }
        self.args_str = "random-args sleep 2"

        self.resource_group = "myResourceGroup"
        self.service = "myService"
        self.job_name = "test-job"

    def test_create_env_list(self):

        env_list = _update_envs(None, self.envs_dict, self.secrets_dict)

        self.assertEquals(4, len(env_list))
        for env in env_list:
            self.assertTrue(isinstance(env, EnvVar))

        self._verify_env_var(env_list[0], "prop1", "value1", None)
        self._verify_env_var(env_list[1], "prop2", "value2", None)
        self._verify_env_var(env_list[2], "secret1", None, "secret_value1")
        self._verify_env_var(env_list[3], "secret2", None, "secret_value2")

    def test_update_env_props_only(self):
        existed_env_list = [
            EnvVar(name="prop1", value="value1"),
            EnvVar(name="prop2", value="value1"),
            EnvVar(name="prop3", value=""),  # This is the case when only key is set
            EnvVar(name="secret1", secret_value="secret_value1"),
            EnvVar(name="secret2", secret_value="secret_value2"),
            EnvVar(name="secret3", secret_value=None),  # Backend won't response value of secret
        ]

        envs_dict = {
            "prop4": "value4"
        }

        secrets_dict = None

        env_list = _update_envs(existed_env_list, envs_dict, secrets_dict)

        self.assertEquals(4, len(env_list))
        for env in env_list:
            self.assertIsNotNone(env)
            self.assertTrue(isinstance(env, EnvVar))

        self._verify_env_var(env_list[0], "prop4", "value4", None)
        self._verify_env_var(env_list[1], "secret1", None, "secret_value1")
        self._verify_env_var(env_list[2], "secret2", None, "secret_value2")
        self._verify_env_var(env_list[3], "secret3", None, None)

    def test_update_env_secrets_only(self):
        existed_env_list = [
            EnvVar(name="prop1", value="value1"),
            EnvVar(name="prop2", value="value2"),
            EnvVar(name="secret1", secret_value="secret_value1"),
            EnvVar(name="secret2", secret_value="secret_value2"),
        ]

        secrets_dict = {
            "secret3": "secret_value3"
        }

        env_list = _update_envs(existed_env_list, None, secrets_dict)

        self.assertEquals(3, len(env_list))
        for env in env_list:
            self.assertIsNotNone(env)
            self.assertTrue(isinstance(env, EnvVar))

        self._verify_env_var(env_list[0], "prop1", "value1", None)
        self._verify_env_var(env_list[1], "prop2", "value2", None)
        self._verify_env_var(env_list[2], "secret3", None, "secret_value3")

    def test_update_secrets(self):
        existed_env_list = [
            EnvVar(name="prop1", value="value1"),
            EnvVar(name="prop2", value="value2"),
            EnvVar(name="secret1", secret_value="secret_value1"),
            EnvVar(name="secret2", secret_value="secret_value2"),
        ]

        secrets = [
            Secret(name="secret3", value="secret_value3")
        ]

        env_list = _update_secrets(existed_env_list, secrets)
        self._verify_env_var(env_list[0], "prop1", "value1", None)
        self._verify_env_var(env_list[1], "prop2", "value2", None)
        self._verify_env_var(env_list[2], "secret3", None, "secret_value3")

    def test_create_args(self):
        args = self.args_str
        target_args = _update_args(None, args)
        self.assertEquals(["random-args", "sleep", "2"], target_args)

    def test_update_args(self):
        args = self.args_str
        target_args = _update_args(["current-args"], args)
        self.assertEquals(["random-args", "sleep", "2"], target_args)

    def test_create_job_properties(self):
        existed_properties = None
        envs = self.envs_dict
        secret_envs = self.secrets_dict
        args = self.args_str
        target_properties = _update_job_properties(existed_properties, envs, secret_envs, args)

        self._verify_env_var(target_properties.template.environment_variables[0], "prop1", "value1", None)
        self._verify_env_var(target_properties.template.environment_variables[1], "prop2", "value2", None)
        self._verify_env_var(target_properties.template.environment_variables[2], "secret1", None, "secret_value1")
        self._verify_env_var(target_properties.template.environment_variables[3], "secret2", None, "secret_value2")
        self.assertEquals(["random-args", "sleep", "2"], target_properties.template.args)

    def test_update_job_properties(self):
        existed_properties = JobResourceProperties(
            template=JobExecutionTemplate(
                environment_variables=[
                    EnvVar(name="prop1", value="value1"),
                    EnvVar(name="secret1", secret_value="secret_value1"),
                ],
                args=["arg1", "arg2"]
            )
        )
        envs = self.envs_dict
        secret_envs = None
        args = self.args_str
        target_properties = _update_job_properties(existed_properties, envs, secret_envs, args)
        self.assertEquals(3, len(target_properties.template.environment_variables))
        self._verify_env_var(target_properties.template.environment_variables[0], "prop1", "value1", None)
        self._verify_env_var(target_properties.template.environment_variables[1], "prop2", "value2", None)
        self._verify_env_var(target_properties.template.environment_variables[2], "secret1", None, "secret_value1")
        self.assertEquals(["random-args", "sleep", "2"], target_properties.template.args)

    def test_is_job_execution_in_final_state(self):
        for status in ("Running", "Pending"):
            self.assertFalse(_is_job_execution_in_final_state(status))

        for status in ("Canceled", "Failed", "Completed"):
            self.assertTrue(_is_job_execution_in_final_state(status))

    @mock.patch('azext_spring.jobs.job.wait_till_end', autospec=True)
    def test_create_asa_job(self, wait_till_end_mock):
        wait_till_end_mock.return_value = None

        client_mock = mock.MagicMock()
        client_mock.job.begin_create_or_update = self._mock_begin_create_or_update
        client_mock.job.get.return_value = sample_job_resource

        result_job = job_create(get_test_cmd(), client_mock, self.resource_group, self.service, self.job_name)
        self.assertEqual(json.dumps(result_job.serialize()), json.dumps(sample_job_resource.serialize()))

    def _mock_begin_create_or_update(self, resource_group, service, name, job_resource: JobResource):
        """
        To validate the request payload is expected.
        """
        self.assertEquals(self.resource_group, resource_group)
        self.assertEquals(self.service, service)
        self.assertEquals(self.job_name, name)
        self.assertEquals(json.dumps(job_resource.serialize(keep_readonly=True)),
                          json.dumps(JobResource.deserialize(json.loads(expected_create_job_payload)).serialize(
                              keep_readonly=True)))
        poller_mock = mock.Mock()
        return poller_mock

    @mock.patch('azext_spring.jobs.job.wait_till_end', autospec=True)
    def test_update_asa_job(self, wait_till_end_mock):
        wait_till_end_mock.return_value = None

        client_mock = mock.MagicMock()
        client_mock.job.get = self._get_job_for_update_job_mock
        client_mock.job.list_env_secrets = self._list_env_secrets_for_update_job_mock
        client_mock.job.begin_create_or_update = self._begin_create_or_update_for_update_job_mock

        self.counter_job_get_in_test_update_asa_job = 0

        job_update(get_test_cmd(), client_mock, self.resource_group, self.service, self.job_name,
                   envs={"prop1": "v_prop1"})

    def _get_job_for_update_job_mock(self, resource_group, service, name):
        if self.counter_job_get_in_test_update_asa_job == 0:
            self.counter_job_get_in_test_update_asa_job += 1
            return self._get_job_for_update_job_mock_0(resource_group, service, name)
        else:
            return self._get_job_for_update_job_mock_1(resource_group, service, name)

    def _get_job_for_update_job_mock_0(self, resource_group, service, name):
        self.assertEquals(self.resource_group, resource_group)
        self.assertEquals(self.service, service)
        self.assertEquals(self.job_name, name)
        return sample_job_resource

    def _get_job_for_update_job_mock_1(self, resource_group, service, name):
        self.assertEquals(self.resource_group, resource_group)
        self.assertEquals(self.service, service)
        self.assertEquals(self.job_name, name)
        return sample_job_resource_after_update

    def _list_env_secrets_for_update_job_mock(self, resource_group, service, name):
        self.assertEquals(self.resource_group, resource_group)
        self.assertEquals(self.service, service)
        self.assertEquals(self.job_name, name)
        return EnvSecretsCollection(
            value=[
                Secret(
                    name="secretKey1",
                    value="secretValue1"
                )
            ]
        )

    def _begin_create_or_update_for_update_job_mock(self, resource_group, service, name, job_resource: JobResource):
        print(json.dumps(job_resource.serialize()))
        self.assertEquals(self.resource_group, resource_group)
        self.assertEquals(self.service, service)
        self.assertEquals(self.job_name, name)
        self.assertEquals(json.dumps(JobResource.deserialize(json.loads(expected_update_job_payload)).serialize()),
                          json.dumps(job_resource.serialize()))
        return None

    def _verify_env_var(self, env: EnvVar, name, value, secret_value):
        self.assertIsNotNone(env)
        self.assertEquals(name, env.name)
        if value is not None:
            self.assertEquals(value, env.value)
            self.assertIsNone(env.secret_value)
        elif secret_value is not None:
            self.assertIsNone(env.value)
            self.assertEquals(secret_value, env.secret_value)
