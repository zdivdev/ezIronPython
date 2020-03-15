# Reference the WPF assemblies
import clr
clr.AddReferenceByName("PresentationFramework, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReferenceByName("PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
clr.AddReference('System.Data')

import System.Windows
from System.Windows import Thickness
from System.Windows import TextWrapping
from System.Windows import HorizontalAlignment
from System.Windows import VerticalAlignment

from System.Windows.Controls import Grid
from System.Windows.Controls import RowDefinition
from System.Windows.Controls import ColumnDefinition
from System.Windows import GridUnitType
from System.Windows import GridLength

from System.Windows.Controls import TabControl
from System.Windows.Controls import TabItem

from System.Windows.Controls import Menu
from System.Windows.Controls import MenuItem
from System.Windows.Controls import ToolTip
from System.Windows.Controls import Separator

from System.Windows.Controls import Label
from System.Windows.Controls import Button
from System.Windows.Controls import CheckBox
from System.Windows.Controls import TextBox
from System.Windows.Controls import ComboBox
from System.Windows.Controls import ListBox
from System.Windows.Controls import ListView
from System.Windows.Controls import ListViewItem
from System.Windows.Controls import GridView
from System.Windows.Controls import GridViewColumn
from System.Windows.Data import Binding

import System.Data
from System.Data import DataTable
from System.Data import DataView
from System.Data import DataColumn
from System.Type import GetType

from Microsoft.Win32 import OpenFileDialog
import System.IO

#
# Control Table
#

_window__ctrl_table = {}

def GetControl(name):
    return _window__ctrl_table.get(name)

def GetWpfControl(name):
    if _window__ctrl_table.get(name): return _window__ctrl_table[name].ctrl;

def DumpControlTable():
    for k,v in _window__ctrl_table.items():
        print(k,v)
        

#
# Dialog
#

def EzAlertDialog(message,title=None):
    from System.Windows import MessageBox
    if title: MessageBox.Show(message,title)
    else: MessageBox.Show(message)

def EzYesNoDialog(message,title,icon=System.Windows.MessageBoxImage.Information):
    return MessageBox.Show(message,title,MessageBoxButton.YesNo,icon)

def EzYesNoCancelDialog(message,title,icon=System.Windows.MessageBoxImage.Information):
    return MessageBox.Show(message,title,MessageBoxButton.YesNoCancel,icon)

def EzFileOpenDialog(initialFile=None,multiselect=False):
    dlg = OpenFileDialog()
    dlg.Multiselect = multiselect
    dlg.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";
    if initialFile: dlg.InitialDirectory = Directory.GetParent(initialFile) #Path.GetFileName(initialFile)
    if dlg.ShowDialog() == True:
        return dlg.FileNames 

#
# Controls
#

class EzControl():
    def Initialize(self,h):
        if h.get('key'): _window__ctrl_table[h['key']] = self
        self.ctrl.Margin  = Thickness(5)
        self.ctrl.Padding = Thickness(5)
    def SetMargin(self,l,t,r,b):
        self.ctrl.Margin = System.Windows.Thickness(l,t,r,b)
    def ShadowEffect(self):
        from System.Windows.Media.Effects import DropShadowBitmapEffect
        self.ctrl.BitmapEffect = DropShadowBitmapEffect()
    def SetFontSize(self,size):
        self.ctrl.FontSize = size
        
class EzLabel(EzControl):
    def __init__(self,h):
        self.ctrl = Label()
        self.Initialize(h)
        if h.get('label'): self.ctrl.Content = h['label']
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        
class EzButton(EzControl):
    def __init__(self,h):
        self.ctrl = Button()
        self.Initialize(h)
        if h.get('label'): self.ctrl.Content = h['label']
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.Click += h['handler']

class EzCheckBox(EzControl):
    def __init__(self,h):
        self.ctrl = CheckBox()
        self.ctrl.VerticalAlignment = VerticalAlignment.Center
        self.ctrl.VerticalContentAlignment = VerticalAlignment.Center
        self.Initialize(h)
        if h.get('label'): self.ctrl.Content = h['label']
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.Click += h['handler']
    def GetValue(self): return self.ctrl.IsChecked

class EzTextBox(EzControl):
    def __init__(self,h):
        self.ctrl = TextBox()
        self.Initialize(h)
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('multiline'): 
            self.ctrl.AcceptsReturn = True
            self.ctrl.AcceptsTab = True
            self.ctrl.TextWrapping = TextWrapping.Wrap
    def Clear(self):
        self.ctrl.Text = ""
    def AppendText(self,text):
        self.ctrl.Text += text
    def SetValue(self,text):
        self.ctrl.Text = text

class EzChoiceBox(EzControl):
    def __init__(self,h):
        self.ctrl = ComboBox()
        self.Initialize(h)
        self.init_ComboBox(h)
    def init_ComboBox(self,h):
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.SelectionChanged += h['handler']
        if h.get('items'):
            self.ctrl.ItemsSource = h['items']
            self.ctrl.SelectedIndex = 0     
    def GetValue(self): return ctrl.Text
    def GetAddedItem(self,args): return args.AddedItems[0]

class EzComboBox(EzChoiceBox):
    def __init__(self,h):
        self.ctrl = ComboBox()
        self.Initialize(h)
        self.init_ComboBox(h)
        self.ctrl.IsEditable=True
        self.ctrl.IsReadOnly=False

class EzListBox(EzControl):
    def __init__(self,h):
        self.ctrl = ListBox()
        self.Initialize(h)
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.SelectionChanged += h['handler']
        if h.get('items'):
            self.ctrl.ItemsSource = h['items']
            self.ctrl.SelectedIndex = 0
    def GetValue(self): return self.ctrl.SelectedItem

class EzListView(EzControl):
    def __init__(self,h):
        self.ctrl = ListView()
        self.table = DataTable('table')
        self.Initialize(h)
        if h.get('fontsize'): self.SetFontSize(h['fontsize'])
        if h.get('handler'): self.ctrl.SelectionChanged += h['handler']
        self.grid = GridView()
        self.grid.AllowsColumnReorder = True; 
        self.grid.ColumnHeaderToolTip = "ListView Column Info";     
        if h.get('columns'): 
            items = h['columns']
            width = None
            if h.get('widths'): width = h['widths']
            for i in range(0,len(items)):
                col = GridViewColumn()
                col.DisplayMemberBinding = Binding(items[i])
                col.Header = items[i]
                if width: col.Width = width[i]
                self.grid.Columns.Add(col);
                self.AddColumn(items[i])     
        self.ctrl.View = self.grid
        self.ctrl.ItemsSource = self.table.DefaultView #DataView(self.table)
        
    def AddColumn(self,label):
        item = DataColumn(label, GetType("System.String"))
        '''
        column.DataType = System.Type.GetType("System.String");
        column.ColumnName = "ParentItem";
        column.AutoIncrement = false;
        column.Caption = "ParentItem";
        column.ReadOnly = false;
        column.Unique = false;        
        '''
        self.table.Columns.Add(item)
    def AddItem(self,items):
        item = self.table.NewRow()
        for key, value in items.items():
            item[key] = value;
        self.table.Rows.Add(item);
    def GetValue(self): 
        return self.ctrl.SelectedItem

            
#
# Containers
#

class EzGrid():
    def __init__(self):
        self.ctrl = Grid()
    def AddRow(self,height=1,expand=False,span=1):
        if expand: length = GridLength(height, GridUnitType.Star)
        else:      length = GridLength(height, GridUnitType.Auto)
        self.ctrl.RowDefinitions.Add(RowDefinition(Height = length))
    def AddColumn(self,width=1,expand=False,span=1):
        if expand: length = GridLength(width, GridUnitType.Star)
        else:      length = GridLength(width, GridUnitType.Auto)
        self.ctrl.ColumnDefinitions.Add(ColumnDefinition(Width = length))
    def AddItem(self,item,row,col,rowspan=1,colspan=1):
        Grid.SetRow(item, row);
        Grid.SetColumn(item, col);
        self.ctrl.Children.Add(item)
        if rowspan > 1: item.SetValue(Grid.RowSpanProperty, rowspan);
        if colspan > 1: item.SetValue(Grid.ColumnSpanProperty, colspan);
        
class EzVBox(EzGrid):
    def __init__(self):
        self.ctrl = System.Windows.Controls.Grid()
        self.rows = 0
    def AddItem(self,item,height=1,expand=False):
        if expand: length = GridLength(height, GridUnitType.Star)
        else:      length = GridLength(height, GridUnitType.Auto)
        self.ctrl.RowDefinitions.Add(RowDefinition(Height = length))
        Grid.SetRow(item, self.rows);
        self.ctrl.Children.Add(item)
        self.rows = self.rows + 1
    def AddSplitter(self,width=1):
        from System.Windows.Controls import GridSplitter
        item = GridSplitter()
        item.HorizontalAlignment = HorizontalAlignment.Stretch
        item.VerticalAlignment = VerticalAlignment.Center
        item.ShowsPreview = True
        item.Height = 5
          
        length = GridLength(width, GridUnitType.Auto)
        self.ctrl.RowDefinitions.Add(RowDefinition(Height = length))
        Grid.SetRow(item, self.rows);
        self.ctrl.Children.Add(item)
        self.rows = self.rows + 1
                 
class EzHBox(EzGrid):
    def __init__(self):
        self.ctrl = System.Windows.Controls.Grid()
        self.cols = 0
    def AddItem(self,item,width=1,expand=False):
        if expand: length = GridLength(width, GridUnitType.Star)
        else:      length = GridLength(width, GridUnitType.Auto)
        self.ctrl.ColumnDefinitions.Add(ColumnDefinition(Width = length))
        Grid.SetColumn(item, self.cols);
        self.ctrl.Children.Add(item)
        self.cols = self.cols + 1
    def AddSplitter(self,width=1):
        from System.Windows.Controls import GridSplitter
        item = GridSplitter()
        item.HorizontalAlignment = HorizontalAlignment.Center
        item.VerticalAlignment = VerticalAlignment.Stretch
        item.ShowsPreview = True
        item.Width = 5
          
        length = GridLength(width, GridUnitType.Auto)
        self.ctrl.ColumnDefinitions.Add(ColumnDefinition(Width = length))
        Grid.SetColumn(item, self.cols);
        self.ctrl.Children.Add(item)
        self.cols = self.cols + 1
                        
class EzBox():
    def __init__(self):
        self.ctrl = StackPanel()
        self.ctrl.Margin = Thickness(15)
    def Add(self,item):
        self.ctrl.Children.Add(item)

class EzTabPane():
    def __init__(self,h):
        self.ctrl = TabControl()
        self.ctrl.Margin =  System.Windows.Thickness(15)
        labels = h.get('labels')
        items = h.get('items')
        if labels and items:
            for i in range(0,len(items)):
                self.AddItem( labels[i], EzLayout(items[i]))  
    def AddItem(self,label,layout):
        tab = TabItem()
        tab.Header = label
        tab.Content = layout
        self.ctrl.Items.Add(tab)

class EzHSplitPane():
    def __init__(self,h):
        self.box = EzHBox()
        self.ctrl = self.box.ctrl
        self.ctrl.Margin =  System.Windows.Thickness(15)
        items = h.get('items')
        width = [ 1, 1 ]
        if h.get('first'):
            width[0] = float(h['first']) * 10
            width[1] = 10 - width[0]
        print( width[0], width[1] )    
        self.box.AddItem(EzLayout(items[0]),width[0],expand=True)
        self.box.AddSplitter()
        self.box.AddItem(EzLayout(items[1]),width[1],expand=True)  

class EzVSplitPane():
    def __init__(self,h):
        self.box = EzVBox()
        self.ctrl = self.box.ctrl
        self.ctrl.Margin =  System.Windows.Thickness(15)
        items = h.get('items')
        self.box.AddItem(EzLayout(items[0]),expand=True)
        self.box.AddSplitter()
        self.box.AddItem(EzLayout(items[1]),expand=True)  
#
# Window
#


class EzMenu():
    def __init__(self,name,menu_table):
        self.ctrl = MenuItem()
        self.ctrl.Header = name;        
        for m in menu_table:
            if not m.get('name') or m['name'] == '-':
                self.ctrl.Items.Add(Separator())
                continue
            if not m.get('item'): continue # Disabled
            if type(m['item']) == list:
                self.ctrl.Items.Add(EzMenu(m['name'],m['item']).ctrl)
            else:
                item = MenuItem()
                if m.get('name'): item.Header = m['name']
                if m.get('item'): item.Click += m['item']
                if m.get('tooltip'): 
                    tooltip =  ToolTip()
                    tooltip.Content = m['tooltip']
                    item.ToolTip = tooltip
                self.ctrl.Items.Add(item)

def EzMenuBar(menu_table):
    ctrl = Menu()
    ctrl.HorizontalAlignment = System.Windows.HorizontalAlignment.Stretch;
    ctrl.VerticalAlignment = System.Windows.VerticalAlignment.Top;
    for m in menu_table:
        ctrl.Items.Add(EzMenu(m['name'],m['item']).ctrl) 
    return ctrl

def EzLayout(content):
    vbox = EzVBox()
    for v in content:
        hbox = EzHBox()
        expand = False
        for h in v:
            name = h.get('name')
            if not name:
                if h.get('expand'): expand = h['expand']
                continue
            if   name == 'Label': f = EzLabel(h)
            elif name == 'Button': f = EzButton(h)
            elif name == 'CheckBox': f = EzCheckBox(h)
            elif name == 'TextField': f = EzTextBox(h)
            elif name == 'TextArea': h['multiline'] = True; f = EzTextBox(h)
            elif name == 'ChoiceBox': f = EzChoiceBox(h)
            elif name == 'ComboBox': f = EzComboBox(h)
            elif name == 'ListBox': f = EzListBox(h)
            elif name == 'Table': f = EzListView(h)
            elif name == 'TabPane': f = EzTabPane(h)
            elif name == 'HSplit': f = EzHSplitPane(h)
            elif name == 'VSplit': f = EzVSplitPane(h)
            else: continue
            '''
            elif name == 'ImageView': f = EzImageView(h,parent)
            elif name == 'ScrollImageView': f = EzScrollImageView(h,parent)
            elif name == 'ToggleButton': f = EzToggleButton(h)
            elif name == 'TreeView': f = EzTreeView(h)
            elif name == 'ProgressBar': f = EzProgressBar(h)
            '''            
            hbox.AddItem(f.ctrl,expand=h.get('expand'))
        vbox.AddItem(hbox.ctrl,expand=expand)
    return vbox.ctrl

class EzWindow(System.Windows.Window):
    def Initialize(self):
        self.createdHandler = None
    def Run(self,title,width,height):
        self.SetTitle(title)
        self.SetSize(width, height)

        self.box = EzVBox()
        if self.menu: self.box.AddItem(EzMenuBar(self.menu),expand=False)
        if self.content: self.box.AddItem(EzLayout(self.content),expand=True)
    
        self.Content = self.box.ctrl
        if self.createdHandler: self.createdHandler()           
        
        System.Windows.Application().Run(self) 
        
    def SetTitle(self,title):
        self.Title = title
    def SetSize(self,width,height):
        self.Width = width
        self.Height = height
    def SetCreatedHandler(self,handler):
        self.createdHandler = handler
        
#
# Application
#

class EzApp(EzWindow):
    def __init__(self):
        self.Initialize()
        self.menu = [
            { 'name' : "File",
              'item' : [
                    { 'name' : "Exit" , 'item' : self.onExit, 'icon' : 'exit.png', 'tooltip' : 'Exit Program' },
                    { 'name' : "-" ,  },
                    { 'name' : "About" , 'item' : self.onAbout, 'icon' : 'exit.png' } ]
            }, { 'name' : "Help",
              'item' : [
                    { 'name' : "About", 'item' : self.onAbout, 'check' : True, 'icon' : 'new.png' } ]
            }]
        tab1 = [[ { "name" : "TextArea", "key" : "text", "expand" : True },
                { 'expand' : True } ]]
        tab2 = [[ { "name" : "ListBox", "items" : [ "apple", "grape" ], 'expand' : True, 'key' : 'listbox', 'handler' : self.onListBox },
                { 'expand' : True } ]]
        tab3 = [[ { "name" : "Table", "columns" : [ "col1", "col2" ], 'widths' : [ 100, 200 ], 'expand' : True, 'key' : 'table', 'handler' : self.onListView },
                { 'expand' : True } ]]
        split1 = [[
                { "name" : "TabPane", "labels" : [ "Tab1", "Tab2", "tab3" ], "items" : [ tab1, tab2, tab3 ], "expand" : True },
                { "expand" : True }, ]]
        split2 = [[ { "name" : "TextArea", 'key' : 'textarea', "expand" : True },
                    { "expand" : True }, ]]
              
        self.content = [ # vbox
            [ # hbox
                { "name" : "Label", "label" : "Address:", "menu" : self.menu },
                { "name" : "TextField", "key" : "textfile", "expand" : True, "menu" : self.menu },
                { "name" : "Button", 'handler' : self.onBrowse, "label" : "Browse", "tooltip" : "About this program" },
            ],         
            [ # hbox
                { "name" : "ChoiceBox", "items" : [ "apple", "grape" ], 'key' : 'choice', 'handler' : self.onChoice },
                { "name" : "ComboBox", "items" : [ "apple", "grape" ] },
                { "name" : "CheckBox", "label" : "Click Me", 'key' : 'check', 'handler' : self.onCheck },
            ], 
            [ # hbox
                { "name" : "HSplit", "items" : [ split1, split2 ] , "first" : 0.5, "expand" : True},
                { "expand" : True },
            ],     
        ]   
        self.SetCreatedHandler(self.onCreated)      

    def onCreated(self):
        listview = GetControl('table')
        listview.AddItem( { "col1":"row1-1", "col2":"row1-2" } )
        listview.AddItem( { "col1":"row2-1", "col2":"row2-2" } )
        listview.AddItem( { "col1":"row3-1", "col2":"row2-2" } )
    def onExit(self, sender, args):
        System.Windows.Application.Current.Shutdown();
    def onAbout(self, sender, args):
        EzAlertDialog("Hello, world!", "My App");
    def onChoice(self, sender, args):
        ctrl = GetControl('choice')
        text = GetControl('text')
        if text and ctrl: text.AppendText("Selected: " + ctrl.GetAddedItem(args) + "\n")
    def onCheck(self, sender, args):
        ctrl = GetControl('check')
        text = GetControl('text')
        if text and ctrl: 
            text.AppendText("Checked: " + ctrl.GetValue().ToString() + "\n")
    def onListBox(self, sender, args):
        ctrl = GetControl('listbox')
        text = GetControl('text')
        if text and ctrl: 
            text.AppendText("List Selected: " + ctrl.GetValue().ToString() + "\n")
    def onListView(self, sender, args):
        ctrl = GetControl('table')
        row = ctrl.GetValue()
        print(row['col1'], row['col2'])
    def onBrowse(self, sender, args):
        ctrl = GetControl('textfile')
        files = EzFileOpenDialog()
        if files: ctrl.SetValue(files[0])
        
if __name__ == "__main__":
    appWin = EzApp()
    appWin.Run("ezWpfPython", 640,400)
    
