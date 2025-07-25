#  Copyright 2008-2015 Nokia Networks
#  Copyright 2016-     Robot Framework Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import pytest
import unittest
import sys
from robotide.spec.libraryfetcher import get_import_result
from robotide.spec.librarymanager import LibraryManager
from utest.resources import DATAPATH

sys.path.append(os.path.join(DATAPATH, 'libs'))


class TestLibraryManager(unittest.TestCase):

    def setUp(self):
        self._keywords = None
        self._library_manager = LibraryManager(':memory:')
        self._library_manager._initiate_database_connection()
        self._library_manager._database.create_database()

    def tearDown(self):
        self._library_manager._database.close()

    def test_database_update(self):
        self._library_manager.fetch_keywords('BuiltIn', '', self._callback)
        keywords = get_import_result('BuiltIn', '')
        self._library_manager._handle_message()
        self.assertFalse(self._library_manager._keywords_differ(keywords, self._keywords))

    def test_manager_handles_callback_exception(self):
        self._library_manager.fetch_keywords('Collections', '', (lambda *_: 1/0))
        self._library_manager._handle_message()
        self._library_manager.fetch_keywords('BuiltIn', '', self._callback)
        self._library_manager._handle_message()
        self.assertTrue(self._keywords is not None)

    def test_fetching_unknown_library(self):
        self._library_manager.fetch_keywords('FooBarZoo', '', self._callback)
        self._library_manager._handle_message()
        self.assertEqual(self._keywords, [])

    @pytest.mark.skip("FAILS since 2.2dev33")
    def test_fetching_from_library_xml(self):
        self._library_manager.fetch_keywords('LibSpecLibrary', '', self._callback)
        self._library_manager._handle_message()
        self.assertEqual(len(self._keywords), 3)

    def test_manager_handler_library_that_throws_timeout_exception(self):
        import sys
        from os import path      # DEBUG import non module
        sys.path.append(path.dirname(path.abspath(__file__)))
        import Exceptional as e
        self._library_manager.fetch_keywords(e.__file__, '', self._callback)
        self._library_manager._handle_message()
        self.assertEqual(self._keywords, [])

    def _callback(self, keywords):
        self._keywords = keywords


if __name__ == '__main__':
    unittest.main()
