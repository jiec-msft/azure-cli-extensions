# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import time

from azure.cli.testsdk import (ScenarioTest, record_only)

# pylint: disable=line-too-long
# pylint: disable=too-many-lines

TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


"""
Due to limitation of this testing framework, not able to 
check the error message for negative cases. However, this
is a good place to hold these negative cases.
"""


@record_only()
class AzureSpringCloudCreateTests(ScenarioTest):
    default_sampling_rate = 10.0

    def test_create_asc_with_ai_basic_case(self):
        self.kwargs.update({
            'serviceName': 'cli-unittest-10',
            'SKU': 'Basic',
            'location': 'eastus',
            'rg': 'cli'
        })
        self.cmd('spring-cloud create -n {serviceName} -g {rg} --sku {SKU} -l {location} '
                 '--no-wait')
        self._wait_service(self.kwargs['rg'], self.kwargs['serviceName'])
        self._test_app_insights_enable_status(self.kwargs['rg'], self.kwargs['serviceName'], True)
        self._clean_service(self.kwargs['rg'], self.kwargs['serviceName'])

    def test_negative_create_asc(self):
        self.kwargs.update({
            'serviceName': 'cli-unittest-10',
            'SKU': 'Basic',
            'location': 'eastus',
            'rg': 'cli',
            'anyString': 'anyString'
        })
        negative_cmd_suffixes = [
            "--disable-app-insights --app-insights {anyString}",
            "--disable-app-insights true --app-insights {anyString}",
            "--disable-app-insights --app-insights-key {anyString}",
            "--disable-app-insights true --app-insights-key {anyString}",
            "--disable-app-insights --sampling-rate 50",
            "--disable-app-insights true --sampling-rate 50",
            "--disable-app-insights --enable-java-agent",
            "--disable-app-insights true --enable-java-agent",
            "--disable-app-insights --enable-java-agent true",
            "--disable-app-insights true --enable-java-agent true",
            "--disable-app-insights --app-insights {anyString} --app-insights-key {anyString}",
            "--disable-app-insights true --app-insights {anyString} --app-insights-key {anyString}",

            "--disable-app-insights --app-insights {anyString} --sampling-rate 50",
            "--disable-app-insights true --app-insights {anyString} --sampling-rate 50",

            "--disable-app-insights --app-insights {anyString} --enable-java-agent",
            "--disable-app-insights --app-insights {anyString} --enable-java-agent true",
            "--disable-app-insights true --app-insights {anyString} --enable-java-agent",
            "--disable-app-insights true --app-insights {anyString} --enable-java-agent true",

            "--disable-app-insights --app-insights {anyString} --app-insights-key {anyString} --sampling-rate 50",
            "--disable-app-insights true --app-insights {anyString} --app-insights-key {anyString} --sampling-rate 50",

            "--disable-app-insights --app-insights-key {anyString} --sampling-rate 50",
            "--disable-app-insights true --app-insights-key {anyString} --sampling-rate 50",

            "--app-insights-key {anyString} --app-insights {anyString}",

            "--sampling-rate -100",
            "--sampling-rate -10",
            "--sampling-rate -1",
            "--sampling-rate -0.1",
            "--sampling-rate 100.1",
            "--sampling-rate 101",
            "--sampling-rate 200",
        ]
        cmd_base = 'az spring-cloud create -g {rg} -n {serviceName} --sku {SKU} -l {location}'
        for suffix in negative_cmd_suffixes:
            cmd = '{} {}'.format(cmd_base, suffix)
            self.cmd(cmd, expect_failure=True)

    def test_asc_update(self):
        self.kwargs.update({
            'serviceName': 'cli-unittest10',
            'rg': 'cli',
            'shared_ai_name': 'cli_scenario_test_20210906102205'
        })
        rg = self.kwargs['rg']
        service_name = self.kwargs['serviceName']

        ai_id, ai_i_key, ai_c_string = self._get_ai_info(rg, self.kwargs['shared_ai_name'])

        self._test_asc_update_with_suffix(
            rg, service_name, True, '--app-insights {}'.format(self.kwargs['shared_ai_name']))

        self._test_asc_update_with_suffix(
            rg, service_name, True, '--app-insights {}'.format(ai_id))

        self._test_asc_update_with_suffix(
            rg, service_name, True, '--app-insights-key {}'.format(ai_i_key))

        self._test_asc_update_with_suffix(
            rg, service_name, True, '--app-insights-key "{}"'.format(ai_c_string))

    def test_negative_asc_update(self):
        self.kwargs.update({
            'serviceName': 'cli-unittest-10',
            'rg': 'cli',
            'anyString': 'anyString'
        })
        negative_cmd_suffixes = [
            "--disable-app-insights --app-insights-key {anyString}",
            "--disable-app-insights --app-insights {anyString}",
            "--disable-app-insights true --app-insights {anyString}",
            "--app-insights-key {anyString} --app-insights {anyString}",
        ]
        cmd_base = 'az spring-cloud update -g {rg} -n {serviceName}'
        for suffix in negative_cmd_suffixes:
            cmd = '{} {}'.format(cmd_base, suffix)
            self.cmd(cmd, expect_failure=True)

    def test_asc_app_insights_update(self):
        self.kwargs.update({
            'serviceName': 'cli-unittest10',
            'rg': 'cli',
            'shared_ai_name': 'cli_scenario_test_20210906102205'
        })
        rg = self.kwargs['rg']
        service_name = self.kwargs['serviceName']
        ai_id, ai_i_key, ai_c_string = self._get_ai_info(rg, self.kwargs['shared_ai_name'])

        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--app-insights {}'.format(self.kwargs['shared_ai_name']))

        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--app-insights {}'.format(ai_id))

        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--app-insights-key {}'.format(ai_i_key))

        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--app-insights-key {}'.format(ai_c_string))

        sampling_rate = 0.0
        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--sampling-rate {}'.format(sampling_rate),
            target_sampling_rate=sampling_rate, disable_ai_first=False)

        sampling_rate = 0.1
        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--sampling-rate {}'.format(sampling_rate),
            target_sampling_rate=sampling_rate, disable_ai_first=False)

        sampling_rate = 1.0
        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--sampling-rate {}'.format(sampling_rate),
            target_sampling_rate=sampling_rate, disable_ai_first=False)

        sampling_rate = 10.0
        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--sampling-rate {}'.format(sampling_rate),
            target_sampling_rate=sampling_rate, disable_ai_first=False)

        sampling_rate = 50.0
        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--sampling-rate {}'.format(sampling_rate),
            target_sampling_rate=sampling_rate, disable_ai_first=False)

        sampling_rate = 99.0
        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--sampling-rate {}'.format(sampling_rate),
            target_sampling_rate=sampling_rate, disable_ai_first=False)

        sampling_rate = 100.0
        self._test_asc_app_insights_update_with_suffix(
            rg, service_name, True, '--sampling-rate {}'.format(sampling_rate),
            target_sampling_rate=sampling_rate, disable_ai_first=False)

    def test_negative_asc_app_insights_update(self):
        self.kwargs.update({
            'serviceName': 'cli-unittest-10',
            'SKU': 'Basic',
            'location': 'eastus',
            'rg': 'cli',
            'anyString': 'anyString'
        })
        negative_cmd_suffixes = [
            # Conflict
            "--app-insights $(anyString) --app-insights-key $(anyString)",
            "--app-insights $(anyString) --app-insights-key $(anyString) --sampling-rate 50",
            "--app-insights $(anyString) --app-insights-key $(anyString) --disable",
            "--app-insights $(anyString) --app-insights-key $(anyString) --disable true",
            "--app-insights $(anyString) --app-insights-key $(anyString) --disable --sampling-rate 50",
            "--app-insights $(anyString) --app-insights-key $(anyString) --disable true --sampling-rate 50",
            "--app-insights $(anyString)  --disable",
            "--app-insights $(anyString)  --disable true",
            "--app-insights $(anyString)  --disable --sampling-rate 50",
            "--app-insights $(anyString)  --disable true --sampling-rate 50",
            "--app-insights-key $(anyString)  --disable",
            "--app-insights-key $(anyString)  --disable true",
            "--disable --sampling-rate 50",
            "--disable true --sampling-rate 50",
            # Invalid sampling-rate
            "--app-insights $(anyString) --sampling-rate -1000",
            "--app-insights $(anyString) --sampling-rate -100",
            "--app-insights $(anyString) --sampling-rate -10",
            "--app-insights $(anyString) --sampling-rate -1",
            "--app-insights $(anyString) --sampling-rate -0.1",
            "--app-insights $(anyString) --sampling-rate 101",
            "--app-insights $(anyString) --sampling-rate 110",
            "--app-insights $(anyString) --sampling-rate 1000",
        ]
        cmd_base = 'az spring-cloud app-insights update -g {rg} -n {serviceName}'
        for suffix in negative_cmd_suffixes:
            cmd = '{} {}'.format(cmd_base, suffix)
            self.cmd(cmd, expect_failure=True)

    def _test_asc_app_insights_update_with_suffix(self, rg, service_name, target_ai_status, cmd_suffix,
                                                  target_sampling_rate=default_sampling_rate,
                                                  disable_ai_first=True):
        if disable_ai_first:
            self._asc_app_insights_update_disable_ai(rg, service_name)
        self.cmd('spring-cloud app-insights update -g {} -n {} --no-wait {}'
                 .format(rg, service_name, cmd_suffix))
        self._wait_ai(rg, service_name)
        self._test_app_insights_enable_status(rg, service_name, target_ai_status)
        self._test_sampling_rate(rg, service_name, target_sampling_rate)

    def _clean_service(self, rg, service_name):
        self.cmd('spring-cloud delete -n {} -g {} --no-wait'
                 .format(service_name, rg))

    def _wait_service(self, rg, service_name):
        for i in range(10):
            result = self.cmd('spring-cloud show -n {} -g {}'.format(service_name, rg)).get_output_in_json()
            if result['properties']['provisioningState'] == "Succeeded":
                break
            elif result['properties']['provisioningState'] == "Failed":
                exit(1)
            sleep_in_seconds = 30
            time.sleep(sleep_in_seconds)

    def _test_asc_update_with_suffix(self, rg, service_name, target_ai_status, cmd_suffix):
        self._asc_update_disable_ai(rg, service_name)
        self.cmd('spring-cloud update -g {} -n {} --no-wait {}'
                 .format(rg, service_name, cmd_suffix))
        self._wait_ai(rg, service_name)
        self._test_app_insights_enable_status(rg, service_name, target_ai_status)

    def _test_app_insights_enable_status(self, rg, service_name, target_status):
        result = self.cmd('spring-cloud app-insights show -n {} -g {}'.format(service_name, rg)).get_output_in_json()
        self.assertEquals(result['traceEnabled'], target_status)

    def _test_sampling_rate(self, rg, service_name, target_sampling_rate):
        result = self.cmd('spring-cloud app-insights show -n {} -g {}'.format(service_name, rg)).get_output_in_json()
        self.assertEquals(result['appInsightsSamplingRate'], target_sampling_rate)

    def _asc_update_disable_ai(self, rg, service_name):
        self.cmd('spring-cloud update -g {} -n {} --disable-app-insights --no-wait'.format(rg, service_name))
        self._wait_ai(rg, service_name)
        self._test_app_insights_enable_status(rg, service_name, False)

    def _asc_app_insights_update_disable_ai(self, rg, service_name):
        self.cmd('spring-cloud app-insights update -g {} -n {} --disable --no-wait'.format(rg, service_name))
        self._wait_ai(rg, service_name)
        self._test_app_insights_enable_status(rg, service_name, False)

    def _wait_ai(self, rg, service_name):
        for i in range(100):
            result = self.cmd('spring-cloud app-insights show -g {} -n {} '
                              '--query "provisioningState" -o tsv'
                              .format(rg, service_name)).output.strip()
            if result == "Succeeded":
                break
            elif result == "Failed":
                exit(1)
            sleep_in_seconds = 3
            time.sleep(sleep_in_seconds)

    def _get_ai_info(self, rg, ai_name):
        response = self.cmd('monitor app-insights component show -g {} --app {}'
                            .format(rg, ai_name)).get_output_in_json()
        ai_id = response['id']
        ai_i_key = response['instrumentationKey']
        ai_c_string = response['connectionString']
        return ai_id, ai_i_key, ai_c_string
