#!/bin/bash

echo Please enter your sudo password if you are prompted to do so.

echo Installing needed packages using apt...
sudo apt install python2 python-tk ffmpeg
echo Done!

echo Running program...
python2 plymouth-creator.py
echo Done!

echo Have a nice day!
