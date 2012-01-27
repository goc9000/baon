# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Jan 23 22:48:58 2012

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainWindow.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.sizer_renames_staticbox = wx.StaticBox(self, -1, "Renamed Files")
        self.sizer_commands_staticbox = wx.StaticBox(self, -1, "Rename Rules")
        self.label_base_path = wx.StaticText(self, -1, "Base Path")
        self.text_base_path = wx.TextCtrl(self, -1, "")
        self.button_browse_base_path = wx.Button(self, -1, "Browse...")
        self.text_commands = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_WORDWRAP)
        self.list_files = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_VRULES|wx.SUNKEN_BORDER)
        self.button_apply = wx.Button(self, wx.ID_APPLY, "")
        self.button_close = wx.Button(self, wx.ID_CLOSE, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self._onEditBasePath, self.text_base_path)
        self.Bind(wx.EVT_BUTTON, self._onBrowseBasePath, self.button_browse_base_path)
        self.Bind(wx.EVT_BUTTON, self._onClickApply, self.button_apply)
        self.Bind(wx.EVT_BUTTON, self._onClickClose, self.button_close)
        # end wxGlade
        
        self._initTable()
        self.Bind(wx.EVT_SIZE, self._onResized, self)

    def __set_properties(self):
        # begin wxGlade: MainWindow.__set_properties
        self.SetTitle("BAON")
        self.SetSize((800, 494))
        self.text_commands.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainWindow.__do_layout
        sizer_master = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_renames = wx.StaticBoxSizer(self.sizer_renames_staticbox, wx.HORIZONTAL)
        sizer_commands = wx.StaticBoxSizer(self.sizer_commands_staticbox, wx.HORIZONTAL)
        sizer_fileset = wx.BoxSizer(wx.HORIZONTAL)
        sizer_fileset.Add(self.label_base_path, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 8)
        sizer_fileset.Add(self.text_base_path, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_fileset.Add(self.button_browse_base_path, 0, 0, 0)
        sizer_master.Add(sizer_fileset, 0, wx.ALL|wx.EXPAND, 8)
        sizer_commands.Add(self.text_commands, 1, wx.ALL|wx.EXPAND, 8)
        sizer_master.Add(sizer_commands, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 8)
        sizer_renames.Add(self.list_files, 1, wx.ALL|wx.EXPAND, 8)
        sizer_master.Add(sizer_renames, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 8)
        sizer_buttons.Add(self.button_apply, 0, wx.RIGHT, 16)
        sizer_buttons.Add(self.button_close, 0, 0, 0)
        sizer_master.Add(sizer_buttons, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.SetSizer(sizer_master)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _initTable(self):
        self.list_files.InsertColumn(0, "From")
        self.list_files.InsertColumn(1, "To")

    def _onResized(self, event):
        width = self.list_files.Size[0] / 2
        self.list_files.SetColumnWidth(0, width)
        self.list_files.SetColumnWidth(1, width)
        event.Skip()

    def showFiles(self, fromList, toList):
        self.list_files.DeleteAllItems()
        for i in range(0, len(fromList)):
            self.list_files.InsertStringItem(i, fromList[i])
            self.list_files.SetStringItem(i, 1, toList[i])
            
    def _onEditBasePath(self, event): # wxGlade: MainWindow.<event_handler>
        print "Event handler `_onEditBasePath' not implemented"
        event.Skip()

    def _onBrowseBasePath(self, event): # wxGlade: MainWindow.<event_handler>
        print "Event handler `_onBrowseBasePath' not implemented"
        event.Skip()

    def _onClickApply(self, event): # wxGlade: MainWindow.<event_handler>
        print "Event handler `_onClickApply' not implemented"
        event.Skip()

    def _onClickClose(self, event): # wxGlade: MainWindow.<event_handler>
        print "Event handler `_onClickClose' not implemented"
        event.Skip()

# end of class MainWindow
