#!/bin/bash
# If necessary, replace the paths below with the full-paths on your computer.
if [ -f fndata-1.6 ]; then
   python3 -i main.py fndata-1.6/   
else
   python3 -i main.py fndata-1.7/
fi
