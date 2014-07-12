#!/bin/sh

# Wait a while to allow the media to be mounted if
# we are being called from a udev rule
sleep 10

# Simply copy the files over to the Camera Uploads dir where they will be
# automagically imported from
cp /media/5508-D13C/DCIM/100_PANA/* "/home/kate/Dropbox/Camera Uploads/"
