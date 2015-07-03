#!/usr/bin/python

import wx

class LootParserApp(wx.Frame):

    def __init__(self, parent, title):

        # derive from the frame __init__() method
        wx.Frame.__init__(self, parent, title=title, size=(300, 300))

        # create the "File" menu and its choices
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        # create a menu bar
        menubar = wx.MenuBar()

        menubar.Append(filemenu, "&File") # add File menu to menubar
        self.SetMenuBar(menubar) # add menubar to frame content

        # create a multiline textbox
        wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # create a status bar at the bottom of the window
        self.CreateStatusBar()

        # set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Show(True)

    def OnAbout(self, e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "A small loot parser", "About Loot Parser", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        # close the frame
        self.Close(True)

# instantiate and run
if __name__ == '__main__':
    app = wx.App()
    frame = LootParserApp(None, 'Loot Parser')
    app.MainLoop()