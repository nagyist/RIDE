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

import unittest
import sys
import os
import pytest

from utest.resources import DATAPATH
from robotide.context import LIBRARY_XML_DIRECTORY
from robotide.spec.xmlreaders import SpecInitializer
from robotide.utils import overrides

sys.path.append(os.path.join(DATAPATH, 'libs'))


class TestLibrarySpec(unittest.TestCase):

    def _spec(self, name):
        return SpecInitializer().init_from_spec(name)

    @pytest.mark.skip("FAILS since 2.2dev33")
    def test_reading_library_from_xml(self):
        kws = self._spec('LibSpecLibrary')
        assert len(kws) == 3
        exp_doc = 'This is kw documentation.\n\nThis is more docs.'
        self._assert_keyword(kws[0], 'Normal Keyword', exp_doc,
                             exp_doc.splitlines()[0], 'ROBOT', '[ foo ]')
        self._assert_keyword(kws[1], 'Attributeless Keyword')
        self._assert_keyword(kws[2], 'Multiarg Keyword',
                             args='[ arg1 | arg2=default value | *args ]')

    @pytest.mark.skip("FAILS since 2.2dev33")
    def test_reading_library_from_old_style_xml(self):
        kws = self._spec('OldStyleLibSpecLibrary')
        assert len(kws) == 3
        exp_doc = 'This is kw documentation.\n\nThis is more docs.'
        self._assert_keyword(kws[0], 'Normal Keyword', exp_doc,
                             exp_doc.splitlines()[0], 'ROBOT', '[ foo ]')
        self._assert_keyword(kws[1], 'Attributeless Keyword')
        self._assert_keyword(kws[2], 'Multiarg Keyword',
                             args='[ arg1 | arg2=default value | *args ]')

    def _assert_keyword(self, kw, name, doc='', shortdoc='', doc_format="ROBOT", args='[  ]'):
        assert kw.name == name
        assert kw.doc == doc, repr(kw.doc)
        assert kw.doc_format == doc_format
        assert kw.shortdoc == shortdoc
        if args:
            assert kw.args == args


class MockedSpecInitializer(SpecInitializer):

    def __init__(self, directories=None, pythonpath_return_value='pythonpath',
                 directory_mapping=None):
        self._pythonpath_return_value = pythonpath_return_value
        if directory_mapping is None:
            directory_mapping = {LIBRARY_XML_DIRECTORY: 'directory'}
        self._directory_mapping = directory_mapping
        self.initialized_from_pythonpath = False
        self.initialized_from_xml_directory = False
        SpecInitializer.__init__(self, directories)

    @overrides(SpecInitializer)
    def _find_from_library_xml_directory(self, directory, name):
        assert(name == 'name')
        self.directory = directory
        return self._directory_mapping.get(directory, None)

    @overrides(SpecInitializer)
    def _find_from_pythonpath(self, name):
        assert(name == 'name')
        return self._pythonpath_return_value

    @overrides(SpecInitializer)
    def _init_from_specfile(self, specfile, name):
        if not specfile:
            return None
        self.initialized_from_pythonpath = (specfile == 'pythonpath')
        self.initialized_from_xml_directory = (specfile == 'directory')
        return 'OK'


class TestSpecInitializer(unittest.TestCase):

    def test_pythonpath_is_preferred_before_xml_directory(self):
        specinitializer = MockedSpecInitializer()
        self.assertEqual('OK', specinitializer.init_from_spec('name'))
        self.assertTrue(specinitializer.initialized_from_pythonpath)
        self.assertFalse(specinitializer.initialized_from_xml_directory)

    def test_default_directory_is_always_used(self):
        specinitializer = MockedSpecInitializer(pythonpath_return_value=None)
        self.assertEqual('OK', specinitializer.init_from_spec('name'))
        self.assertFalse(specinitializer.initialized_from_pythonpath)
        self.assertTrue(specinitializer.initialized_from_xml_directory)
        self.assertEqual(specinitializer.directory, LIBRARY_XML_DIRECTORY)

    def test_not_finding_correct_file(self):
        specinitializer = MockedSpecInitializer(
            pythonpath_return_value=None, directory_mapping={})
        self.assertEqual(None, specinitializer.init_from_spec('name'))
        self.assertFalse(specinitializer.initialized_from_pythonpath)
        self.assertFalse(specinitializer.initialized_from_xml_directory)

    def test_finding_from_given_directory(self):
        specinitializer = MockedSpecInitializer(
            directories=['my_dir'], pythonpath_return_value=None,
            directory_mapping={'my_dir': 'directory'})
        self.assertEqual('OK', specinitializer.init_from_spec('name'))
        self.assertFalse(specinitializer.initialized_from_pythonpath)
        self.assertTrue(specinitializer.initialized_from_xml_directory)
        self.assertEqual(specinitializer.directory, 'my_dir')


if __name__ == '__main__':
    unittest.main()

