import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

#from System.Windows.Forms import Shortcut, MainMenu, MenuItem
from System.Windows.Forms import Application, Form
from System.Windows.Forms import MenuStrip, StatusBar
from System.Windows.Forms import ToolStripContainer, TextImageRelation
from System.Windows.Forms import ToolStripMenuItem, ToolStripSeparator
from System.Windows.Forms import ToolStrip, ToolStripButton, ToolStripLabel, ToolStripTextBox
from System.Windows.Forms import BorderStyle, ToolStripItemDisplayStyle
from System.Drawing import Size, Image, Point

_window__ctrl_table = {}

#
# Controls
#

class Control():
    def __init__(self):
        self.Dock = DockStyle.Fill
        self.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right

#
# Windows
#

def EzMenu(name,menu_table):
    menu = ToolStripMenuItem(name)
    for m in menu_table:
        if not m.get('name') or m['name'] == '-':
            menu.DropDownItems.Add(ToolStripSeparator())
            continue
        if not m.get('item'): continue # Disabled
        if type(m['item']) == list:
            menu.DropDownItems.Add(EzMenu(m['name'],m['item']))
        else:
            item = ToolStripMenuItem(m['name'],None,m['item'])
            #item.Text += m['name']
            #item.Click += m['item']
            if m.get('icon'): item.Image = Image.FromFile(m['icon'])
            if m.get('check'): item.Checked = True
            menu.DropDownItems.Add(item)
    return menu

def EzMenuBar(parent,menubar_table):
    menubar = MenuStrip()
    menubar.Parent = parent         
    for m in menubar_table:
        menubar.Items.Add(EzMenu(m['name'],m['item'])) 
    return menubar

def EzToolBar(parent,toolbar_table):
    toolbar = ToolStrip()
    #toolbar.Location = Point(0, 0);
    #toolbar.ImageScalingSize = Size(20, 20);
    for m in toolbar_table:
        print(m)
        if not m.get('name') or m['name'] == '-':
            toolbar.Items.Add(ToolStripSeparator())
            continue
        if m['name'] == "Button":
            item = ToolStripButton()
            if m.get('handler'): item.Click += m['handler']
            if m.get('label'): item.Text = m['label']
            if m.get('icon'):  item.Image = Image.FromFile(m['icon'])
            item.DisplayStyle = ToolStripItemDisplayStyle.ImageAndText;
            item.TextImageRelation = TextImageRelation.ImageAboveText;
        elif m['name'] == "Label":
            item = ToolStripLabel()
            if m.get('label'): item.Text = m['label']
        elif m['name'] == 'TextBox':
            item = ToolStripTextBox()
            if m.get('handler'): item.KeyDown += m['handler']
            if m.get('text'): item.Text += m['text']
            item.BorderStyle = BorderStyle.FixedSingle;
        else:
            continue      
        toolbar.Items.Add(item)
    return toolbar

def EzStatusBar(parent):
    statusbar = StatusBar()
    statusbar.Parent = parent
    return statusbar

def Border(parent):
    border = ToolStripContainer()
    border.TopToolStripPanelVisible = false;
    border.RightToolStripPanelVisible = false;
    border.BottomToolStripPanelVisible = false;
    border.LeftToolStripPanelVisible = false;
            
class Window(Form):
    def CreateWindow(self,title,width,height):
        self.ctrl = _window__ctrl_table
        self.Text = title
        self.Size = Size(width,height)
        self.mb = EzMenuBar(self,self.menu)
        self.tb = EzToolBar(self,self.tool)
        self.sb = EzStatusBar(self)
        self.Controls.Add(self.tb)
        self.Controls.Add(self.mb)
        self.CenterToScreen()        
    def SetStatusText(self,text):
        self.sb.Text = text

#
# Application
#
      
class MonoApp(Window):
    def __init__(self):
        self.menu = [
            { 'name' : "File",
              'item' : [
                    { 'name' : "Exit" , 'item' : self.onExit, 'icon' : 'exit.ico' },
                    { 'name' : "-" ,  },
                    { 'name' : "Exit" , 'item' : self.onExit, 'icon' : 'exit.ico' } ]
            }, { 'name' : "Help",
              'item' : [
                    { 'name' : "About", 'item' : self.onAbout, 'check' : True, 'icon' : 'new.ico' } ]
            }]
        self.tool = [
                { "name" : "Label",   "label" : "File:",  },
                { "name" : "TextBox", "handler" : self.onExit,   },
                { "name" : "Button",  "label" : "Exit", 'icon' : 'exit.png', "handler" : self.onExit, "tooltip" : "Quit"  },
            ]
        self.content = [ # vbox
            [ # hbox
                { "name" : "Label", "label" : "Address:" },
                { "name" : "TextField", "key" : "text", "expand" : True },
                { "name" : "Button",  "label" : "Browse", "tooltip" : "Open File", "handler" : self.onBrowse  },
                { "name" : "Button",  "label" : "About", "handler" : self.onAbout  },
            ],
            [ # hbox
                { "name" : "TextArea", "expand" : True },
                { "expand" : True },
            ],               
        ]
        self.CreateWindow("ezIronPython Demo", 640, 400)
        self.SetStatusText("Ready")
    def onExit(self, sender, event):
        self.Close()
    def onAbout(self, sender, event):
        self.Close()
    def onBrowse(self, sender, event):
        self.Close()
        
if __name__ == '__main__':
    Application.Run(MonoApp())
