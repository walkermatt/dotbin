#!/bin/bash

# Author: Matt Walker (@_walkermatt)
#
# Script to allow you to set the primary monitor on Linux.
# The primary monitor usually displays your panels.
# When run the script displays each monitor it finds in turn
# and prompts y/n to make it the primary monitor.
#
# Usage:
#   Make this file executable (chmod u+x set-primary-monitor.sh)
#   Run it and press y to select a monitor (./set-primary-monitor.sh)
#
# Inspiration: http://ubuntuforums.org/showthread.php?t=1309247

displays=$(xrandr --prop | grep "[^dis]connected" | cut --delimiter=" " -f1) # query connected monitors
for display in $displays
do
    echo "Used display: $display? (y/N)"
    # Read the users input, suppress echoing the input
    # and read only one character (we are only
    # interested in y or Y)
    read -s -n 1 choice
    case $choice in
        [yY]) xrandr --output $display --primary
        ;;
    esac
done

