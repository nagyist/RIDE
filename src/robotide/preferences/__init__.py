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

from .editor import PreferenceEditor
from .editors import GridEditorPreferences, TextEditorPreferences, TestRunnerPreferences
from .general import DefaultPreferences
from .imports import ImportPreferences
from .saving import SavingPreferences
from .settings import Settings, initialize_settings, RideSettings
from ..ui import ExcludePreferences

import wx


class Languages:
    names = [('Bulgarian', 'bg', wx.LANGUAGE_BULGARIAN), ('Bosnian', 'bs', wx.LANGUAGE_BOSNIAN),
             ('Czech', 'cs', wx.LANGUAGE_CZECH), ('German', 'de', wx.LANGUAGE_GERMAN),
             ('English', 'en', wx.LANGUAGE_ENGLISH), ('Spanish', 'es', wx.LANGUAGE_SPANISH),
             ('Finnish', 'fi', wx.LANGUAGE_FINNISH), ('French', 'fr', wx.LANGUAGE_FRENCH),
             ('Hindi', 'hi', wx.LANGUAGE_HINDI), ('Italian', 'it', wx.LANGUAGE_ITALIAN),
             ('Dutch', 'nl', wx.LANGUAGE_DUTCH), ('Polish', 'pl', wx.LANGUAGE_POLISH),
             ('Portuguese', 'pt', wx.LANGUAGE_PORTUGUESE),
             ('Brazilian Portuguese', 'pt-BR', wx.LANGUAGE_PORTUGUESE_BRAZILIAN),
             ('Romanian', 'ro', wx.LANGUAGE_ROMANIAN), ('Russian', 'ru', wx.LANGUAGE_RUSSIAN),
             ('Swedish', 'sv', wx.LANGUAGE_SWEDISH), ('Thai', 'th', wx.LANGUAGE_THAI),
             ('Turkish', 'tr', wx.LANGUAGE_TURKISH), ('Ukrainian', 'uk', wx.LANGUAGE_UKRAINIAN),
             ('Vietnamese', 'vi', wx.LANGUAGE_VIETNAMESE),
             ('Chinese Simplified', 'zh-CN', wx.LANGUAGE_CHINESE_SIMPLIFIED),
             ('Chinese Traditional', 'zh-TW', wx.LANGUAGE_CHINESE_TRADITIONAL)]


class Preferences(object):

    def __init__(self, settings):
        self.settings = settings
        self._preference_panels = []
        self._add_builtin_preferences()

    @property
    def preference_panels(self):
        return self._preference_panels

    def add(self, preference_ui):
        if preference_ui not in self._preference_panels:
            self._preference_panels.append(preference_ui)

    def remove(self, panel_class):
        if panel_class in self._preference_panels:
            self._preference_panels.remove(panel_class)

    def _add_builtin_preferences(self):
        self.add(DefaultPreferences)
        self.add(SavingPreferences)
        self.add(ImportPreferences)
        self.add(GridEditorPreferences)
        self.add(TextEditorPreferences)
        self.add(TestRunnerPreferences)
        self.add(ExcludePreferences)
