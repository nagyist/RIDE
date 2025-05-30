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
import wx
from wx import Colour, BitmapBundle


class ButtonWithHandler(wx.Button):

    def __init__(self, parent, label, mk_handler=None, handler=None, width=-1, bitmap=None,
                 height=25, color_secondary_foreground='black', color_secondary_background='light grey', fsize=10):
        fsize = max(8, fsize)
        bt_image = None
        style = 0
        name = label
        if bitmap is not None and isinstance(bitmap, str):
            img_path = os.path.join(os.path.dirname(__file__), bitmap)
            bt_image = BitmapBundle.FromFiles(img_path)
            label = 'config_panel'
            width = height
            style = wx.BU_EXACTFIT | wx.BU_NOTEXT | wx.BORDER_NONE
        if width == -1:
            width = len(label) * fsize
        size = wx.Size(width, height)
        wx.Button.__init__(self, parent, label=label, size=size, style=style, name=name)
        if bt_image is not None:
            self.SetBitmap(bt_image)
            self.SetBitmapLabel(bt_image)
            self.SetToolTip(name)
        self.SetBackgroundColour(Colour(color_secondary_background))
        self.SetOwnBackgroundColour(Colour(color_secondary_background))
        self.SetForegroundColour(Colour(color_secondary_foreground))
        # self.SetOwnForegroundColour(Colour(color_secondary_foreground))
        if not handler or mk_handler:
            if not mk_handler:
                name = 'on_%s' % label.strip().replace(' ', '_').lower()
            else:
                name = 'on_%s' % mk_handler.strip().replace(' ', '_').lower()
            handler = getattr(parent, name)
        parent.Bind(wx.EVT_BUTTON, handler, self)
