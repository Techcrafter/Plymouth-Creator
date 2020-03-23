import os
import Tkinter, tkFileDialog
from subprocess import call

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

videoInputFile = ""
videoOutputDirectory = ""

name = ""
delay = 0

root = Tkinter.Tk()
root.withdraw()

class Handler:
  def on_selectVideoButton_clicked(self, button):
    global videoInputFile
    videoInputFile = tkFileDialog.askopenfilename(parent=root,initialdir="/home",title='Select your .mp4 video',filetypes = (("mp4 files","*.mp4"),("all files","*.*")))
    selectVideoDoneLabel.set_text("Done!")
  def on_selectVideoOutputButton_clicked(self, button):
    global videoOutputDirectory
    videoOutputDirectory = tkFileDialog.askdirectory(parent=root,initialdir="/home",title='Select an empty output directory')
    selectVideoOutputDoneLabel.set_text("Done!")
  def on_startVideoConvertionButton_clicked(self, button):
    os.system("ffmpeg -i '" + videoInputFile + "' '" + videoOutputDirectory + "/image-%01d.png' -hide_banner")
    videoConvertionDoneLabel.set_text("Done!")
  def on_selectDirectoryButton_clicked(self, button):
    outputDirectory = tkFileDialog.askdirectory(parent=root,initialdir="/home",title='Select directory with .png files')
    selectDirectoryDoneLabel.set_text("Done!")
  def on_generateButton_clicked(self, button):
    name = nameEntry.get_text()
    delay = int(delayEntry.get_text())
    #GERNERATE SETUP AND CONFIG FILES HERE
    generationDoneLabel.set_text("Done!")

builder = Gtk.Builder()
builder.add_from_file("plymouth-creator.glade")
builder.connect_signals(Handler())

selectVideoDoneLabel = builder.get_object("selectVideoDoneLabel")
selectVideoOutputDoneLabel = builder.get_object("selectVideoOutputDoneLabel")
videoConvertionDoneLabel = builder.get_object("videoConvertionDoneLabel")

nameEntry = builder.get_object("nameEntry")
delayEntry = builder.get_object("delayEntry")

selectDirectoryDoneLabel = builder.get_object("selectDirectoryDoneLabel")
generationDoneLabel = builder.get_object("generationDoneLabel")

window1 = builder.get_object("window1")
window1.connect("delete-event", Gtk.main_quit)
window1.show_all()

Gtk.main()
