# -*- coding: utf-8 -*-

import clr
clr.AddReference('System.Core')
clr.AddReference('StdLib')
#clr.AddReferenceToFileAndPath(r"C:\Lib\dll\StdLib.dll")
clr.AddReferenceToFileAndPath(r"C:\Lib\dll\ezPyWpfLib.dll")
import ezPyWpfLib as ez
import os
import codecs
import base64

import System
from System.IO import *
from System.Net import *

global appWin

def setStatusText(text):
    status = ez.GetControl('status')
    ez.RunLater(status.ctrl,lambda : status.SetValue(text))

def setTableRow(row,text):
    def setTableRow1():
        row[1] = text
    table = ez.GetControl('list')
    ez.RunLater(table.ctrl,setTableRow1)

def onCreated():
    ez.DumpControlTable()

def onClosing(event):
    if not ez.YesNoDialog("Do you want to quie ?","Quit"):
        event.args.Cancel = True

def onOpen(event):
    dirname = ez.DirectoryOpenDialog()
    text = ez.GetControl('directory')
    text.SetValue(dirname)
    dirlist = ez.GetControl('list')
    dirlist.AddRow([dirname,"Ready"])
    
def onDrop(event):
    text = ez.GetControl('directory')
    dirlist = ez.GetControl('list')
    for f in event:
        if System.IO.Directory.Exists(f):
            text.SetValue(f)  
            dirlist.AddRow([f,"Ready"])  
            
def onClear(event):
    table = ez.GetControl('list')
    table.Clear()
  
def htmlAddImg( f, image_file ):
    with open( image_file, "rb" ) as infile:
        data = base64.b64encode(infile.read())
        f.write(b'<img src="data:image/png;base64,' + data + b'" /><br>\n')

def imgToHtml(base_dir,row):
    image_files = os.listdir(base_dir)
    html_file = base_dir + ".html"
    with open( html_file, "wb" ) as f:
        for image_file in image_files:
            print(image_file)
            image_file_path = os.path.join(base_dir,image_file)
            htmlAddImg( f, image_file_path )
            print(image_file_path )
        print( '->', html_file )

def imgsToHtmls(args):
    sub_dirs = os.listdir(args[0])
    i = 1;
    setTableRow(args,"%d / %d" % (0, len(sub_dirs)))
    for sub_dir in sub_dirs:
        sub_dir_path = os.path.join(args[0],sub_dir)
        if os.path.isdir( sub_dir_path ):
            setStatusText( sub_dir_path )
            imgToHtml( sub_dir_path, args )
        setTableRow(args,"%d / %d" % (i, len(sub_dirs)))
        i = i + 1
    setTableRow(args,"%d OK" % len(sub_dirs))
    
def onRun(event):
    setStatusText("Started")
    table = ez.GetControl('list')
    rows = table.Select()
    for r in rows:
        ez.StartThread(imgsToHtmls,args=[r])

app_status = [
        { "name" : "Label", "label" : "Ready", 'key' : 'status' },
        { "name" : "Spacer" },
    ]
    
app_content = [ # vbox  
    [ # hbox
        { "name" : "Label", 'label' : "Directory", "width" : 60, "expand" : False, 'border' : False},
        { "name" : "TextField", 'key' : 'directory', "drop" : onDrop, "expand" : True, 'border' : False},
        { "name" : "Button", "label" : "Open", 'handler' : onOpen, 'width' : 40, "expand" : False, 'border' : False},
        { "expand" : False, 'border' : True  },
    ], 
    [ # hbox
        { "name" : "TableView", 'columns' : ["Directory","Status"], "key" : "list", "expand" : True, 'border' : False},
        { "expand" : True, 'border' : True  },
    ], 
    [ # hbox
        { "name" : "Spacer" },
        { "name" : "Button", 'label' : "Clear", 'handler' : onClear, "expand" : False, 'width' : 40, 'border' : False},
        { "name" : "Button", 'label' : "Run", 'handler' : onRun, "expand" : False, 'width' : 40, 'border' : False},
        { "expand" : False, 'border' : True  },
    ],     
]


def MakeWindow():
    win = ez.Window()
    win.SetTitle("ImageToHtml")
    win.SetSize(320,240)
    win.SetStatusBar(app_status)
    win.SetContent(app_content)
    win.SetCreatedHandler(onCreated)  
    win.SetCloseHandler(onClosing)
    win.SetFileDropHandler(onDrop)
    return win

if __name__ == "__main__":
    global appWin
    appWin = MakeWindow()
    appWin.Run()




