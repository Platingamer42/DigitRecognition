#Dear reader,
#when I wrote this code, only god and me knew what it does.
#Now only god knows.
#However, if you want to understand this or even want to improve it's performance,
#please hold this counter up-to-date:

#Hours wasted on this project: 152

import mnist_loader, numpy, sys, os, time
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
        self.RandomPicker = RandomPicker()
        self.TextOut.addText("[J.A.R.V.I.S.]: Dataset loadeded!")
        self.env = 0
        try:
            import picamera
            self.camera = picamera.PiCamera()

        except ImportError:
            self.env = 1
        except picamera.exc.PiCameraError:
            self.env = 1        
        if self.env == 0:
            os.system("vcgencmd display_power 1")
            self.TextOut.addText("[J.A.R.V.I.S.]: Initializing!")
        else:
            self.TextOut.addText("[J.A.R.V.I.S.]: I couldn't find a camera! You won't be able to take pictures.")
        self.TextOut.addText("[J.A.R.V.I.S.]: Loading AI!")
        self.ai = AI_LITE()
        self.TextOut.addText("[J.A.R.V.I.S.]: Loading ImageEditor!")
        #time.sleep(3)
        self.PicEditor = PicEditor()
        #self.TextOut.reset()
        self.GUI.drawMain()

        self.ai.initialize()
        self.TextOut.addText("[J.A.R.V.I.S.]: Everything's done, Sir.") 
        self.GUI.handler()
        

    def sendThroughAI(self, x):
        values = self.ai.feedforward(x)
        digit = numpy.argmax(values)
        return [digit, values]
        
    def runImage(self):
        img = Image.open("data/image_RAW.png").convert("L") #Black-White!
        #img = self.PicEditor.recolor(img) #Calls the function that returns the image, but the white pixels are whiter and the black are blacker!
        if min(img.getdata()) == 255:
            self.TextOut.addText("[J.A.R.V.I.S.]: I can't handle this picture. It's all-white!")
            return [False]
        img = self.PicEditor.recolor(img)
        img = self.PicEditor.removeWhites(img) #Now we are ready to remove the white rows and collums (on each side) - We just don't need them.
        all = self.PicEditor.getAll(img)
        if not all[0]:
            img = self.PicEditor.resize(img)    
            img = self.PicEditor.recenter(img)
            return [True, [img]]
        return [True, all[1], all[2]]

    def takeAShot(self):
        if self.env == 1:
            self.TextOut.addText("[J.A.R.V.I.S.]: You have no camera installed. I will pick the last picture that was made.")
            return False
        
        #A higher resolution might be "more beautiful", 
        #but since we don't need it exactly and it only speeds the translation down
        #this should be ok.
        self.TextOut.addText("[J.A.R.V.I.S.] Running... This might need a moment.")
        self.camera.resolution = (300,300)
        self.camera.brightness = 80 #We don't want it dark!
                        
        self.camera.capture("data/image_RAW.png")


    #Get a png and translate it... - Returns an array containing arrays (1 pxl = 1 array...)
    def translateToMNIST(self, path,img=None):
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
