#!/bin/bash

echo Please enter your sudo password if you are prompted to do so!

echo Installing dependencies using apt...
sudo apt install python3 python3-gi python3-tk ffmpeg
echo Done!

echo Running program...
python3 plymouth-creator.py
echo Done!

echo Have a nice day!
