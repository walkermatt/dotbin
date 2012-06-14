#!/bin/sh

# Change to the directory that this script lives in
base_dir=`dirname $0`
cd $base_dir

# Wait a while to allow the media to be mounted if
# we are being called from a udev rule
sleep 10

src_dir=/media/5508-D13C/DCIM/100_PANA/
dest_dir=/home/kate/Dropbox/Photos/

./importphotos.py --copy --src_dir $src_dir --dest_dir $dest_dir >> importphotos.log
