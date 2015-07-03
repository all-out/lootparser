#!/usr/bin/python

# demo script taken from:
# http://www.pythoncentral.io/introduction-python-gui-development/

import wx

class ExampleApp(wx.Frame):

    def __init__(self):
        # every wx app must create one App object before it does anything
        # else using wx
        self.app = wx.App()

        # set up main window
        wx.Frame.__init__(self,
                          parent=None,
                          title='wxPython Example',
                          size=(300,200))

        # the greetings available
        self.greetings = ['hello', 'goodbye', 'heyo']

        # layout panel and hbox
        self.panel = wx.Panel(self, size=(300, 200))
        self.box = wx.BoxSizer(wx.VERTICAL)

        # greeting combobox
        self.greeting = wx.ComboBox(parent=self.panel,
                                    value='hello', 
                                    size=(280,-1), 
                                    choices=self.greetings)
        # add the greeting combo to the hbox
        self.box.Add(self.greeting, 0, wx.TOP)
        self.box.Add((-1, 10))

        # recipient entry
        self.recipient = wx.TextCtrl(parent=self.panel,
                                     size=(280, -1),
                                     value='world')
        # add the recipient textctrl to the hbox
        self.box.Add(self.recipient, 0, wx.TOP)

        # add padding to lower the button position
        self.box.Add((-1, 100))

        # the go button
        self.go_button = wx.Button(self.panel, 10, 'Go')
        # bind an event for the go button
        self.Bind(wx.EVT_BUTTON, self.print_result, self.go_button)
        # make the button the default action of the form
        self.go_button.SetDefault()
        # add the button to the hbox
        self.box.Add(self.go_button, 0, flag=wx.ALIGN_RIGHT|wx.BOTTOM)
        
        # tell the panel to use the hbox
        self.panel.SetSizer(self.box)

    def print_result(self, *args):
        '''Print greeting constructed from the selections made by the user.'''
        print('%s, %s' % (self.greeting.GetValue().title(),
                          self.recipient.GetValue()))

    def run(self):
        '''Run the app.'''
        self.Show()
        self.app.MainLoop()

# instantiate and run
app = ExampleApp()
app.run()
