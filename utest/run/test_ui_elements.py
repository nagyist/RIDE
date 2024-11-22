#  Copyright 2024-     Robot Framework Foundation
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
import time
import unittest
import os
import pytest

DISPLAY = os.getenv('DISPLAY')
if not DISPLAY:  # Avoid failing unit tests in system without X11
    pytest.skip("Skipped because of missing DISPLAY", allow_module_level=True)
import wx
from wx.lib.agw.aui import AuiManager

from robotide.robotapi import (TestDataDirectory, TestCaseFile, ResourceFile,
                               TestCase, UserKeyword)
from robotide.spec.librarymanager import LibraryManager
from robotide.ui.mainframe import ActionRegisterer, ToolBar, AboutDialog
from robotide.ui.actiontriggers import MenuBar, ShortcutRegistry
from robotide.application import Project
from robotide.controller.filecontrollers import (TestDataDirectoryController,
                                                 ResourceFileController)
from utest.resources import FakeSettings, FakeEditor
from robotide.ui import treeplugin as st
from robotide.ui import treenodehandlers as th
from robotide.publish import PUBLISHER
from robotide.ui.treeplugin import Tree
from robotide.namespace.namespace import Namespace
from robotide.log import LogOutput

th.FakeDirectorySuiteHandler = th.FakeUserKeywordHandler = \
    th.FakeSuiteHandler = th.FakeTestCaseHandler = \
    th.FakeResourceHandler = th.TestDataDirectoryHandler
st.Editor = lambda *args: FakeEditor()
Tree._show_correct_editor = lambda self, x: None
Tree.get_active_datafile = lambda self: None
Tree._select = lambda self, node: self.SelectItem(node)

app = wx.App()


class _AboutDialog(AboutDialog):

    def __init__(self, frame, controller):
        self.frame = frame
        self.controller = controller.controller
        super(_AboutDialog, self).__init__()
        self.model = controller

    def _execute(self):
        print(f"DEBUG: _execute at AboutDialog nothing to do"
              f" using font={self.font_face}")

    def show_dialog(self):
        self.ShowDialog()

    def ShowDialog(self):
        self._execute()
        wx.CallLater(1000, self.Destroy)
        self.ShowModal()
        self.Destroy()


class _BaseDialogTest(unittest.TestCase):

    def setUp(self):
        settings = FakeSettings()
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.frame.tree = Tree(self.frame, ActionRegisterer(AuiManager(self.frame),
                                                            MenuBar(self.frame), ToolBar(self.frame),
                                                            ShortcutRegistry(self.frame)), settings)
        # self.frame.Show()
        self.model = self._create_model()

    def tearDown(self):
        PUBLISHER.unsubscribe_all()
        # wx.CallAfter(self.app.ExitMainLoop)
        self.app.ExitMainLoop()
        self.app.Destroy()
        self.app = None

    def _create_model(self):
        suite = self._create_directory_suite('/top_suite')
        suite.children = [self._create_file_suite('sub_suite_%d.robot' % i)
                          for i in range(3)]
        res = ResourceFile()
        res.source = 'resource.robot'
        res.keyword_table.keywords.append(UserKeyword(res, 'Resource Keyword', ['en']))
        library_manager = LibraryManager(':memory:')
        library_manager.create_database()
        model = Project(
            Namespace(FakeSettings()), library_manager=library_manager)
        model.controller = TestDataDirectoryController(suite)
        rfc = ResourceFileController(res, project=model)
        model.resources.append(rfc)
        model.insert_into_suite_structure(rfc)
        return model

    def _create_directory_suite(self, source):
        return self._create_suite(TestDataDirectory, source, is_dir=True)

    def _create_file_suite(self, source):
        suite = self._create_suite(TestCaseFile, source)
        suite.testcase_table.tests = [TestCase(
            suite, '%s Fake Test %d' % (suite.name, i)) for i in range(16)]
        return suite

    @staticmethod
    def _create_suite(suite_class, source, is_dir=False):
        suite = suite_class()
        suite.source = source
        if is_dir:
            suite.directory = source
        suite.keyword_table.keywords = [
            UserKeyword(suite.keyword_table, '%s Fake UK %d' % (suite.name, i), ['en'])
            for i in range(5)]
        return suite


class TestLogOutput(_BaseDialogTest):

    def test_log_output(self):
        log_output = LogOutput(self.frame)
        assert log_output._output is not None
        log_output.update_log()
        time.sleep(1)
        log_output.update_log("String value")
        time.sleep(1)
        log_output.update_log(['line one', 'line two'])
        time.sleep(1)
        # self.frame.Maximize()
        sim = wx.UIActionSimulator()
        sim.KeyDown(keycode=wx.WXK_CONTROL_A)
        time.sleep(5)
        log_output.close()
        # print(f"DEBUG: TestLogOutput: final {log_output._output.GetStatus()}")


if __name__ == '__main__':
    unittest.main()
    app.Destroy()
