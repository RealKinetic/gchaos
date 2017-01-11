# MIT License

# Copyright (c) 2017 Real Kinetic

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest

from mock import MagicMock
from mock import patch

from gchaos.config import CHAOS_CONFIG
from gchaos.gae.datastore.actions import ACTIONS
from gchaos.gae.datastore.errors import trigger as trigger_errors
from gchaos.gae.datastore.hook import get_config_and_trigger
from gchaos.gae.datastore.hook import trigger_action


@patch('gchaos.gae.datastore.hook.get_config_and_trigger')
class TriggerActionErrorTests(unittest.TestCase):

    def test_name_not_in_actions(self, get_config_and_trigger_mock):
        """Ensure if the name is not in the actions that no subsequent calls
        are made.
        """
        name = "foo"

        ds_config = CHAOS_CONFIG.datastore

        trigger_action(name, ds_config)

        get_config_and_trigger_mock.assert_not_called()

    def test_name_in_actions(self, get_config_and_trigger_mock):
        """Ensure if the name is in the actions that subsequent calls are made.
        """
        name = ACTIONS.GET

        ds_config = CHAOS_CONFIG.datastore

        trigger_action(name, ds_config)

        get_config_and_trigger_mock.assert_called_once_with(
            name, ds_config.errors, trigger_errors)


class GetConfigAndTriggerTestCase(unittest.TestCase):

    def test_no_config(self):
        """Ensure if the action doesn't return a config doesn't trigger."""
        name = "foo"

        trigger_func = MagicMock()

        error_config = CHAOS_CONFIG.datastore.errors
        error_config.get_by_action = MagicMock(return_value=None)

        get_config_and_trigger(name, error_config, trigger_func)

        error_config.get_by_action.assert_called_once_with(name)
        trigger_func.assert_not_called()

    def test_error_config_exists(self):
        """Ensure if the action does return a config for errors does trigger."""
        name = "foo"

        trigger_func = MagicMock()

        error_config = CHAOS_CONFIG.datastore.errors
        error_config.get_by_action = MagicMock(
            return_value=error_config.get_errors)

        get_config_and_trigger(name, error_config, trigger_func)

        error_config.get_by_action.assert_called_once_with(name)
        trigger_func.assert_called_once_with(error_config.get_errors)

    def test_latency_config_exists(self):
        """Ensure if the action does return a config for latency does trigger."""
        name = "foo"

        trigger_func = MagicMock()

        latency_config = CHAOS_CONFIG.datastore.latency
        latency_config.get_by_action = MagicMock(
            return_value=latency_config.get_latencies)

        get_config_and_trigger(name, latency_config, trigger_func)

        latency_config.get_by_action.assert_called_once_with(name)
        trigger_func.assert_called_once_with(latency_config.get_latencies)
