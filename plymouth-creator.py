import os
import glob
import Tkinter, tkFileDialog
from subprocess import call

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

videoInputFile = ""
videoOutputDirectory = ""

outputDirectory = ""

name = ""
description = ""
loopAnimation = None
scaleImages = None

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
    global outputDirectory
    outputDirectory = tkFileDialog.askdirectory(parent=root,initialdir="/home",title='Select directory with .png files')
    selectDirectoryDoneLabel.set_text("Done!")
  def on_generateButton_clicked(self, button):
    global name
    global description
    global scaleImages
    name = nameEntry.get_text()
    description = descriptionEntry.get_text()
    loopAnimation = loopAnimationCheckButton.get_active()
    scaleImages = scaleImagesCheckButton.get_active()
    amountOfPngFiles = len(glob.glob1(outputDirectory,"*.png"))
    plymouthFile = open(outputDirectory + "/" + name + ".plymouth","w")
    plymouthFile.write("[Plymouth Theme]\n")
    plymouthFile.write("Name=" + name + "\n")
    plymouthFile.write("Description=" + description + "\n")
    plymouthFile.write("ModuleName=script\n")
    plymouthFile.write("\n")
    plymouthFile.write("[script]\n")
    plymouthFile.write("ImageDir=/usr/share/plymouth/themes/" + name + "\n")
    plymouthFile.write("ScriptFile=/usr/share/plymouth/themes/" + name + "/" + name + ".script")
    plymouthFile.close()
    scriptFile = open(outputDirectory + "/" + name + ".script","w")
    scriptFile.write("Window.SetBackgroundTopColor (0, 0, 0);\n")
    scriptFile.write("Window.SetBackgroundBottomColor (0, 0, 0);\n")
    scriptFile.write("for(i = 1; i <= " + str(amountOfPngFiles) + "; i++)\n")
    scriptFile.write("{\n")
    if(scaleImages == False):
      scriptFile.write("  image[i].image = Image(\"image-\" + i + \".png\");\n")
    else:
      scriptFile.write("  image[i].image = Image(\"image-\" + i + \".png\").Scale(Window.GetWidth(), Window.GetHeight());\n")
    scriptFile.write("  image[i].sprite = Sprite(image[i].image);\n")
    scriptFile.write("  image[i].sprite.SetOpacity(0);\n")
    scriptFile.write("  image[i].x = Window.GetX() + Window.GetWidth() / 2 - image[i].image.GetWidth() / 2;\n")
    scriptFile.write("  image[i].y = Window.GetY() + Window.GetHeight() / 2 - image[i].image.GetHeight() / 2;\n")
    scriptFile.write("  image[i].sprite.SetPosition(image[i].x, image[i].y, 0);\n")
    scriptFile.write("}\n")
    scriptFile.write("\n")
    scriptFile.write("index = 1;\n")
    scriptFile.write("fun boot_callback()\n")
    scriptFile.write("{\n")
    scriptFile.write("  if(index >= " + str(amountOfPngFiles) + " + 1)\n")
    scriptFile.write("  {\n")
    if(loopAnimation == False):
      scriptFile.write("    image[" + str(amountOfPngFiles) + "].sprite.SetOpacity(1);\n")
    else:
      scriptFile.write("    index = 1;\n")
    scriptFile.write("  }\n")
    scriptFile.write("  else\n")
    scriptFile.write("  {\n")
    scriptFile.write("    for(i = 1; i <= " + str(amountOfPngFiles) + "; i++)\n")
    scriptFile.write("    {\n")
    scriptFile.write("      if(index != i)\n")
    scriptFile.write("      {\n")
    scriptFile.write("        image[i].sprite.SetOpacity(0);\n")
    scriptFile.write("      }\n")
    scriptFile.write("      else\n")
    scriptFile.write("      {\n")
    scriptFile.write("        image[i].sprite.SetOpacity(1);\n")
    scriptFile.write("      }\n")
    scriptFile.write("    }\n")
    scriptFile.write("    index++;\n")
    scriptFile.write("  }\n")
    scriptFile.write("}\n")
    scriptFile.write("\n")
    scriptFile.write("Plymouth.SetRefreshFunction(boot_callback);\n")
    scriptFile.write("Plymouth.SetQuitFunction(boot_callback);")
    scriptFile.close()
    installFile = open(outputDirectory + "/install.sh","w")
    installFile.write("#!/bin/bash\n")
    installFile.write("echo Please enter your sudo password if you are prompted to do so.\n")
    installFile.write("echo Installing the " + name + " theme...\n")
    installFile.write("sudo mkdir /usr/share/plymouth/themes/" + name + "\n")
    installFile.write("sudo cp -rf ./ /usr/share/plymouth/themes/" + name + "\n")
    installFile.write("sudo update-alternatives --quiet --install /usr/share/plymouth/themes/default.plymouth default.plymouth /usr/share/plymouth/themes/" + name + "/" + name + ".plymouth 100\n")
    installFile.write("sudo update-alternatives --quiet --set default.plymouth /usr/share/plymouth/themes/" + name + "/" + name + ".plymouth\n")
    installFile.write("sudo update-initramfs -u\n")
    installFile.write("echo Done!\n")
    installFile.write("echo Testing...\n")
    installFile.write("sudo plymouthd\n")
    installFile.write("sudo plymouth --show-splash\n")
    installFile.write("sleep 10\n")
    installFile.write("sudo plymouth quit\n")
    installFile.write("echo Done!\n")
    installFile.write("echo Have a nice day!")
    installFile.close()
    os.system("chmod +x " + outputDirectory + "/install.sh")
    testFile = open(outputDirectory + "/test.sh","w")
    testFile.write("#!/bin/bash\n")
    testFile.write("echo Please enter your sudo password if you are prompted to do so.\n")
    testFile.write("echo Testing...\n")
    testFile.write("sudo plymouthd\n")
    testFile.write("sudo plymouth --show-splash\n")
    testFile.write("sleep 10\n")
    testFile.write("sudo plymouth quit\n")
    testFile.write("echo Done!\n")
    testFile.write("echo Have a nice day!")
    testFile.close()
    os.system("chmod +x " + outputDirectory + "/test.sh")
    uninstallFile = open(outputDirectory + "/uninstall.sh","w")
    uninstallFile.write("#!/bin/bash\n")
    uninstallFile.write("echo Please enter your sudo password if you are prompted to do so.\n")
    uninstallFile.write("echo Uninstalling the " + name + " theme...\n")
    uninstallFile.write("sudo update-alternatives --quiet --remove default.plymouth /usr/share/plymouth/themes/" + name + "/" + name + ".plymouth\n")
    uninstallFile.write("sudo rm -rf /usr/share/plymouth/themes/" + name + "\n")
    uninstallFile.write("sudo update-alternatives --quiet --auto default.plymouth\n")
    uninstallFile.write("sudo update-initramfs -u\n")
    uninstallFile.write("echo Done!\n")
    uninstallFile.write("echo Testing...\n")
    uninstallFile.write("sudo plymouthd\n")
    uninstallFile.write("sudo plymouth --show-splash\n")
    uninstallFile.write("sleep 10\n")
    uninstallFile.write("sudo plymouth quit\n")
    uninstallFile.write("echo Done!\n")
    uninstallFile.write("echo Have a nice day!")
    uninstallFile.close()
    os.system("chmod +x " + outputDirectory + "/uninstall.sh")
    generationDoneLabel.set_text("Done!")

builder = Gtk.Builder()
builder.add_from_file("plymouth-creator.glade")
builder.connect_signals(Handler())

selectVideoDoneLabel = builder.get_object("selectVideoDoneLabel")
selectVideoOutputDoneLabel = builder.get_object("selectVideoOutputDoneLabel")
videoConvertionDoneLabel = builder.get_object("videoConvertionDoneLabel")

nameEntry = builder.get_object("nameEntry")
descriptionEntry = builder.get_object("descriptionEntry")
loopAnimationCheckButton = builder.get_object("loopAnimationCheckButton")
scaleImagesCheckButton = builder.get_object("scaleImagesCheckButton")

selectDirectoryDoneLabel = builder.get_object("selectDirectoryDoneLabel")
generationDoneLabel = builder.get_object("generationDoneLabel")

window1 = builder.get_object("window1")
window1.connect("delete-event", Gtk.main_quit)
window1.show_all()

Gtk.main()
