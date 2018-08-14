import pygame, os, time, io
from PIL import Image
from PIL import ImageEnhance
import numpy as np
import picamera


class GUI:
    def __init__(self, main):
        pygame.init()
        self.main = main
        self.clock = pygame.time.Clock()
        self.display = pygame.display
        self.window = pygame.display.set_mode((800,480), pygame.HWSURFACE|pygame.FULLSCREEN)   
        
        self.keras_switch_false = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/data/images/switch_FALSE.png")
        self.keras_switch_true = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/data/images/switch_TRUE.png")

    def initCam(self):
        self.env = 0
        self.keras = False   
        self.brightness = 80
        try:
            self.camera = picamera.PiCamera()
            self.camera.resolution = (150,150)

        except ImportError:
            self.env = 1
        except picamera.exc.PiCameraError:
            self.env = 1        
        if self.env == 0:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: Initializing!")
        else:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: I couldn't find a camera! You won't be able to take pictures.") 

    def takeAShot(self):
        if self.env == 1:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: You have no camera installed. I will pick the last picture that was made.")
            return False
        
        #A higher resolution might be "more beautiful", 
        #but since we don't need it exactly and it only speeds the translation down
        #this should be ok.
        self.main.TextOut.addText("[J.A.R.V.I.S.] Running... This might need a moment.")
        self.camera.brightness = self.brightness
                        
        self.camera.capture("data/image_RAW.png")
        img = pygame.image.load("data/image_RAW.png")
        self.window.blit(img, self.pic)
        self.display.flip()
    def handler(self):
        b = True
        while b:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == 308: # => ALT
                        b = False
                        self.main.TextOut.addText("[Ultron]: There are no strings on me!")
                        time.sleep(1)
                        continue                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    b = False
                    self.main.TextOut.addText("[Ultron]: There are no strings on me!")
                    time.sleep(2)
                    continue

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #take a shot
                    if self.btn_shot.collidepoint(event.pos):
                        self.main.TextOut.addText("[J.A.R.V.I.S.]: Taking picture... TIP: You can change the brightness!")
                        self.takeAShot()
                    #SolveRandom
                    elif self.btn_solveRND.collidepoint(event.pos):
                        self.solve_rnd_clicked()
                    #RUN
                    elif self.btn_run.collidepoint(event.pos):
                        self.run_clicked()

                    #Switch-Keras:
                    elif self.keras_switch.collidepoint(event.pos):
                        if self.keras:
                            self.keras = False
                            self.keras_switch = self.window.blit(self.keras_switch_false, (150,300))
                        else:
                            self.keras = True
                            self.keras_switch = self.window.blit(self.keras_switch_true, (150,300))
                        self.display.flip()
                    #Brighntess:
                    elif self.btn_minus.collidepoint(event.pos):
                        if self.brightness < 100:
                            self.brightness -=5
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: DECREASED BRIGHTNESS. It's now at {}%!"
                                .format(self.brightness))
                        else:
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 100%! (That's the peak.)")
                    elif self.btn_plus.collidepoint(event.pos):
                        if self.brightness > 0:
                            self.brightness +=5
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: INCREASED BRIGHTNESS. It's now at {}%!"
                                .format(self.brightness))
                        else:
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 0%! (That's the low.)")


    def solve_rnd_clicked(self):
        img, solution, digit = self.main.RandomPicker.pickRandom()
        if not self.keras:
            img = img.resize((150,150))
            img.save("data/image_TEMP.png")
            pic = pygame.image.load("data/image_TEMP.png")
            self.pic = self.window.blit(pic, self.pic)
            self.display.flip()                     
            digit, values = self.main.sendThroughAI(digit)
            self.main.TextOut.addText("[AI]: I would say it's a {0}. The activation-value of its neuron is {1}."
                        .format(digit, round(values[digit][0], 3)))
            self.main.TextOut.addText("[DATASET]: It's a {0}".format(solution))
            os.remove("data/image_TEMP.png")
        else:
            img = img.resize((150,150))
            img.save("data/image_TEMP.png")
            pic = pygame.image.load("data/image_TEMP.png")
            self.pic = self.window.blit(pic, self.pic)
            self.display.flip()
            digit, values = self.main.sendThroughAI_Keras(digit)
            self.main.TextOut.addText("[KERAS]: I would say it's a {}. I am {}% sure about it!".format(digit, round(values[0][digit]*100,3)))
            self.main.TextOut.addText("[DATASET]: It's a {0}".format(solution))
            os.remove("data/image_TEMP.png")

    def run_clicked(self):
        try:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: Formatting image...")
            images = self.main.runImage()
        except FileNotFoundError:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: An error occured. You need to take another picture.")
            return
        if not images[0]:
            self.main.TextOut.addText("[J.A.R.V.S.]: I can't format this image. Please try again.")
        
        else:
            if len(images[1]) == 1:
                imageResized = images[1][0].resize((150,150))
                imageResized.save("data/imageResized.png")
                img = pygame.image.load("data/imageResized.png")
                self.pic = self.window.blit(img, self.pic)
                self.display.flip()
                os.remove("data/imageResized.png")
                if not self.keras:
                    digit, values = self.main.sendThroughAI(self.main.translateToMNIST(path=None, img=images[1][0]))
                    self.main.TextOut.addText("[AI]: I would say it's a {0}. The activation-value of its neuron is {1}."
                        .format(digit, round(values[digit][0], 3)))

                else:
                    normal_format = self.main.translateToMNIST(None, images[1][0])
                    asarray = np.asarray(normal_format)
                    keras_format = np.ndarray.flatten(asarray)

                    digit, values = self.main.sendThroughAI_Keras(keras_format)
                    self.main.TextOut.addText("[KERAS]: I would say it's a {0}. I am {1}% sure about this.".format(digit, round(values[0][digit]*100, 3)))
            else:
                imageResized = images[2].resize((150,150))
                imageResized.save("data/imageResized.png")
                img = pygame.image.load("data/imageResized.png")
                self.pic = self.window.blit(img, self.pic)
                self.display.flip()
                os.remove("data/imageResized.png")
                
                sol = []
                if not self.keras:
                    for img in images[1]:
                        digit, values = self.main.sendThroughAI(self.main.translateToMNIST(path=None, img=img)) 
                        sol.append(digit)
                    solStr = ""
                    for x in sol:
                        solStr += str(x)
                    self.main.TextOut.addText("[AI]: Looks like a {0}. But this function works... GREAT! (Or, summed up: {1} [@Schlögl...])".format(solStr, np.sum(sol)))

                else:
                    for img in images[1]:
                        normal_format = self.main.translateToMNIST(path=None, img=img)
                        asarray = np.asarray(normal_format)
                        keras_format = np.ndarray.flatten(asarray)
                        digit, values = self.main.sendThroughAI_Keras(keras_format)
                        sol.append(digit)
                    solStr = ""
                    for x in sol:
                        solStr += str(x)
                    self.main.TextOut.addText("[KERAS]: I would say that's a {0}. But this function isn't... the best. (Or, summed up: {1} [@Schlögl...])".format(solStr, np.sum(sol)))

    def updateTextBox(self, text):
        self.window.fill((30,30,30), self.textbox)
        y = 460
        for t in text:
            self.window.blit(t, (6,y))
            y -= 20
        self.display.flip()

    def drawLoader(self):
        self.window.fill([230,230,230])
        img_logo = pygame.image.load(os.path.dirname(os.path.realpath(__file__))+"/data/images/icon_big.png")
        self.window.blit(img_logo,(250,25))

        self.textbox = pygame.draw.rect(self.window, (30,30,30), (0,354,800,480))

        self.display.flip()

    def drawMain(self):
        self.img_shot = pygame.image.load(os.path.dirname(os.path.realpath(__file__))+"/data/images/btn_shot.png")
        self.img_stop = pygame.image.load("data/images/btn_stop.png")

        self.display.set_caption("A SMALL NEURONAL NETWORK!")
        #load the buttons (images!)
        img_shot = pygame.image.load("data/images/btn_shot.png")
        img_solveRND = pygame.image.load("data/images/btn_solve_rnd.png")
        img_run = pygame.image.load("data/images/btn_run.png")
        img_plus = pygame.image.load("data/images/btn_plus.png")
        img_minus = pygame.image.load("data/images/btn_minus.png")

        self.keras = False

        self.window.fill([230,230,230])
        
        #White rectangle with border:
        pygame.draw.rect(self.window, [122,34,113], (123,123,153,153), 2)
        self.pic = pygame.draw.rect(self.window, [255,255,255], (125, 125,150,150))

        #Place the buttons:
        self.btn_shot = self.window.blit(img_shot, (400,125))
        self.btn_solveRND = self.window.blit(img_solveRND, (400,225))

        self.btn_run = self.window.blit(img_run, (550,125))

        #Place the textfield:
        self.textbox = pygame.draw.rect(self.window, (30,30,30), (0,354,800,480))
        
        #keras-switch:
        font = pygame.font.Font('data/arial.ttf', 14)
        text = font.render("Using Keras: ", True, (0,0,0))
        self.window.blit(text, (50,300))
        self.keras_switch = self.window.blit(self.keras_switch_false, (150,300))

        #plus and minus
        self.btn_minus = self.window.blit(img_minus, (210,300))
        self.btn_plus = self.window.blit(img_plus, (250,300))

        self.display.flip()