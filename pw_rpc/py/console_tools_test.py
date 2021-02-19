#!/usr/bin/env python3
# Copyright 2021 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Tests encoding HDLC frames."""

import unittest
from unittest import mock

from pw_rpc.console_tools import CommandHelper, Watchdog


class TestWatchdog(unittest.TestCase):
    """Tests the Watchdog class."""
    def setUp(self):
        self._reset = mock.Mock()
        self._expiration = mock.Mock()
        self._while_expired = mock.Mock()

        self._watchdog = Watchdog(self._reset, self._expiration,
                                  self._while_expired, 99999)

    def _trigger_timeout(self):
        # Don't wait for the timeout -- that's too flaky. Call the internal
        # timeout function instead.
        self._watchdog._timeout_expired()  # pylint: disable=protected-access

    def test_expiration_callbacks(self):
        self._watchdog.start()

        self._expiration.not_called()

        self._trigger_timeout()

        self._expiration.assert_called_once_with()
        self._while_expired.assert_not_called()

        self._trigger_timeout()

        self._expiration.assert_called_once_with()
        self._while_expired.assert_called_once_with()

        self._trigger_timeout()

        self._expiration.assert_called_once_with()
        self._while_expired.assert_called()

    def test_reset_not_called_unless_expires(self):
        self._watchdog.start()
        self._watchdog.reset()

        self._reset.assert_not_called()
        self._expiration.assert_not_called()
        self._while_expired.assert_not_called()

    def test_reset_called_if_expired(self):
        self._watchdog.start()
        self._trigger_timeout()

        self._watchdog.reset()

        self._trigger_timeout()

        self._reset.assert_called_once_with()
        self._expiration.assert_called()


class TestCommandHelper(unittest.TestCase):
    def setUp(self) -> None:
        self._commands = {'command_a': 'A', 'command_B': 'B'}
        self._helper = CommandHelper(self._commands, 'The header',
                                     'The footer')

    def test_help_contents(self):
        help_contents = self._helper.help()

        self.assertTrue(help_contents.startswith('The header'))
        self.assertIn('The footer', help_contents)

        for cmd_name in self._commands:
            self.assertIn(cmd_name, help_contents)

    def test_repr_is_help(self):
        self.assertEqual(repr(self._helper), self._helper.help())


if __name__ == '__main__':
    unittest.main()
