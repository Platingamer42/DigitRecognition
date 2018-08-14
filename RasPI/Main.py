#!/usr/bin/env python

#Dear reader,
#when I wrote this code, only god and me knew what it does.
#Now only god knows.
#However, if you want to understand this or even want to improve it's performance,
#please hold this counter up-to-date:

#Hours wasted on this project: 160

import numpy, sys, os, time
from MNIST_LOADER import MNIST_LOADER
from AI_LITE_Keras import AI_LITE_Keras
from GUI import GUI
from PIL import Image
from TextOut import TextOut
from AI_LITE import AI_LITE
from RandomPicker import RandomPicker
from PicEditor import PicEditor

class Main:
    def __init__(self):
        #start the gui!
        self.GUI = GUI(self)
        self.GUI.drawLoader()

        self.TextOut = TextOut(self.GUI)
        self.TextOut.addText("[J.A.R.V.I.S.]: Loading Dataset! This could need a second!")
        self.mnist_loader = MNIST_LOADER()
        self.mnist_loader.loadMNIST()
        self.TextOut.addText("[J.A.R.V.I.S.]: Dataset loadeded!")
        self.RandomPicker = RandomPicker(self.mnist_loader)
        self.TextOut.addText("[J.A.R.V.I.S.]: Loading AI!")
        self.ai = AI_LITE()
        self.ai_keras = AI_LITE_Keras()
        self.TextOut.addText("[J.A.R.V.I.S.]: Loading ImageEditor!")
        self.PicEditor = PicEditor()
        self.TextOut.addText("[J.A.R.V.I.S.]: Loading Camera!")
        self.GUI.initCam()
        self.GUI.drawMain()

        self.ai.initialize()
        self.TextOut.addText("[J.A.R.V.I.S.]: Everything's done, Sir.") 
        self.GUI.handler()
        

    def sendThroughAI(self, x):
        values = self.ai.feedforward(x)
        digit = numpy.argmax(values)
        return [digit, values]
        
    def sendThroughAI_Keras(self, x):
        x = (numpy.expand_dims(x, 0))
        values = self.ai_keras.sendThrough(x)
        digit = numpy.argmax(values)
        return [digit,values]

    def runImage(self):
        img = Image.open("data/image_RAW.png").convert("L") #Black-White!
        img = self.PicEditor.recolor(img) #Calls the function that returns the image, but the white pixels are whiter and the black are blacker!
        if min(img.getdata()) == 255:
            self.TextOut.addText("[J.A.R.V.I.S.]: I can't handle this picture. It's all-white!")
            return [False]
        img = self.PicEditor.removeWhites(img) 
        all = self.PicEditor.getAll(img)
        if not all[0]:
            img = self.PicEditor.resize(img)    
            img = self.PicEditor.recenter(img)
            return [True, [img]]
        return [True, all[1], all[2]]

    #Get a png and translate it... - Returns an array containing arrays (1 pxl = 1 array...)
    def translateToMNIST(self, path=None,img=None):
        if img == None:
            #just in case it's not in greyscale yet.
            img = Image.open(path).convert('L')
            data = list(img.getdata())
            newData = []
            for x in data:
                newData.append([(255 - x) / 255])
            return newData
        #Not working via path, but via a img directly:
        data = list(img.getdata())
        newData = []
        for x in data:
            newData.append([(255-x) / 255])
        return newData
        
main = Main()
