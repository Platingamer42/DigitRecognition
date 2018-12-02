#!/bin/sh
sudo bash -c "echo 1 > /sys/class/backlight/rpi_backlight/bl_power"		

cd ~/Workspaces/Python/DigitRecognition/RasPI/
python3 Main.py
$SHELL