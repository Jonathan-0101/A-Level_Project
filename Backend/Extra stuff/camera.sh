#!/bin/bash
DATE=$(date + %d-%m-%y_%H%M)
ffmpeg -f v4l2 -r 25 -s 640x480 -i /dev/video0 $DATE.avi
