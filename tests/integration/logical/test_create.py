# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test 'create'.
"""

import time
import unittest

from stratisd_client_dbus import StratisdErrorsGen

from stratis_cli._main import run
from stratis_cli._errors import StratisCliRuntimeError

from .._constants import _DEVICES

from .._misc import _device_list
from .._misc import Service


class CreateTestCase(unittest.TestCase):
    """
    Test creating a volume w/out a pool.
    """
    _MENU = ['filesystem', 'create']
    _POOLNAME = 'deadpool'
    _VOLNAMES = ['oubliette', 'mnemosyne']

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testCreation(self):
        """
        Creation of the volume must fail since pool is not specified.
        """
        command_line = self._MENU + [self._POOLNAME] + self._VOLNAMES
        with self.assertRaises(StratisCliRuntimeError) as ctxt:
            all(run(command_line))
        expected_error = StratisdErrorsGen.get_object().POOL_NOTFOUND
        self.assertEqual(ctxt.exception.rc, expected_error)


@unittest.skip("Creation of a volume could fail if no room in pool.")
class Create2TestCase(unittest.TestCase):
    """
    Test creating a volume w/ a pool.
    """
    _MENU = ['filesystem', 'pool', 'create']
    _POOLNAME = 'deadpool'
    _VOLNAMES = ['oubliette', 'mnemosyne']

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        command_line = \
           ['pool', 'create'] + [self._POOLNAME] + \
           [d.device_node for d in _device_list(_DEVICES, 1)]
        all(run(command_line))

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testCreation(self):
        """
        Creation of the volume should succeed since pool is available.
        """
        command_line = self._MENU + [self._POOLNAME] + self._VOLNAMES
        all(run(command_line))


class Create3TestCase(unittest.TestCase):
    """
    Test creating a volume w/ a pool when volume of same name already exists.
    """
    _MENU = ['filesystem', 'create']
    _POOLNAME = 'deadpool'
    _VOLNAMES = ['oubliette', 'mnemosyne']

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        command_line = \
           ['pool', 'create'] + [self._POOLNAME] + \
           [d.device_node for d in _device_list(_DEVICES, 1)]
        all(run(command_line))
        command_line = self._MENU + [self._POOLNAME] + self._VOLNAMES
        all(run(command_line))

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testCreation(self):
        """
        Creation of this volume should fail, because there is an existing
        volume of the same name.
        """
        command_line = self._MENU + [self._POOLNAME] + self._VOLNAMES
        with self.assertRaises(StratisCliRuntimeError) as ctxt:
            all(run(command_line))
        expected_error = StratisdErrorsGen.get_object().LIST_FAILURE
        self.assertEqual(ctxt.exception.rc, expected_error)
