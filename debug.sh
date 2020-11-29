#!/bin/bash

echo Running "plymouth-creator.py"...
python2 plymouth-creator.py
echo Done!

echo Waiting...
read null
echo Done!

echo ---NEXT SESSION BEGIN------------------------------------------------
./debug.sh
