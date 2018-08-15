DISCLAIMER:
This project is really messy - I will clean it up soon. 

This package contains 3 different versions of my DigitRecognition-System:

1) The "RasPI-Old"-Version:
Since I couldn't manage to run tensorflow, keras and scipy on my rasbperry pi at the beginning, I had to improvise.
So I created this Version (You could say it's a "light" version) without a keras-implementation.

2) The Windows-Version:
This Version was the updated, but not running, version of the "RasPi-Old"-Version. It comes with a Video-Stream and keras.
ATTENTION:
If you have multiple cameras connected to your PC (e.g. a webcam in your laptop + a webcam via usb) you have to edit the line
'cv2.VideoCapture(0)' in GUI.startStream() and try other numbers in the constructor
(0, 1, 2 - depends on how many cameras you have installed).

3) The updated RasPi-Version:
This version was created when I finally figured out how to run the Windows-Version on the RasPI. 
It's quite similar to the said version, yet it doesn't use openCV for the video stream, since there is no openCV-module
available on the PI (You could compile it from source and try it, if you know how)


Version 1 and 2 were tested on a RasPI 3 and are designed for use with the 7'' LCD-Display. The PI was running Raspbian 
Stretch (latest version as of 25.07.2018) and using tensorflow 1.9 as backend for keras (Version 2.2.0).

Version 3 was tested on a Desktop-PC running Windows 7 and on a laptop running Windows 10. Windows 10 threw some warnings, 
but it worked fine. (Maybe there were some version-mismatches; the laptop wasn't up do date)


If installing tensorflow and the other modules doesn't work on YOUR Pi, you might check this: 
https://medium.com/@abhizcc/installing-latest-tensor-flow-and-keras-on-raspberry-pi-aac7dbf95f2
(You might need to pic other wheel-files, though)

NOTICE:
Besides this file, there also is a "LICENSE" File. Please read it.

If you get any errors with this script, you may have permission to ask for my help. But don't expect too much, since I will
not tell you how you can contact me.

I also commented links to code-snippets I found on pages like stackoverflow or snippets that inspired me at some point.


INSTALLATION:
- You will need python3 (Any Version should work) and following python-packages:
- Tensorflow [backend] (You should be able to use theano as backend instead)
- keras
- scipy
- numpy
- opencv (Only on Windows; the PI-Version doesn't need it)


Last updated: Today.
