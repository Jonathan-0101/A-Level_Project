#!/bin/bash
$ timeout 30s tail -f /var/log/pacman.log
DATE=$(date +"%Y-%m-%d_%H%M")
ffmpeg -f v4l2 -r 25 -s 640x480 -i /dev/video0 $DATE.avi