import pygame, os, time
from PIL import Image
from PIL import ImageEnhance
import numpy as np
import cv2

class GUI:
    def __init__(self, main):
        pygame.init()
        self.main = main
        self.clock = pygame.time.Clock()
        self.display = pygame.display
        self.window = pygame.display.set_mode((700,600), pygame.HWSURFACE)   
        
        self.keras_switch_false = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/data/images/switch_FALSE.png")
        self.keras_switch_true = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/data/images/switch_TRUE.png")
        self.keras = False    
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
                        self.main.TextOut.addText("[J.A.R.V.I.S.]: Starting stream. This might need a second. Click this button again, if you're finished...")

                        self.startStream()
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
                            self.keras_switch = self.window.blit(self.keras_switch_false, (150,370))
                        else:
                            self.keras = True
                            self.keras_switch = self.window.blit(self.keras_switch_true, (150,370))
                        self.display.flip()
                    elif self.btn_minus.collidepoint(event.pos):
                        self.main.TextOut.addText("[J.A.R.V.I.S.]: This button is used to decrease the stream brightness.")
                        self.main.TextOut.addText("It has no power here. *screams in king Theoden*")
                    elif self.btn_plus.collidepoint(event.pos):
                        self.main.TextOut.addText("[J.A.R.V.I.S.]: This button is used to increase the stream brightness.")
                        self.main.TextOut.addText("It has no power here. *screams in king Theoden*")


    #This stream produces BGR-Pictures; but it actually doesn't matter in this project.
    def startStream(self):
        vc = cv2.VideoCapture(0)
        if vc.isOpened(): # try to get the first frame
            val, frame = vc.read()
        else:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: I couldn't find a camera. Sorry.")
            vc.release()
            return
        self.btn_shot = self.window.blit(self.img_stop, self.btn_shot)
        factor = 2.5 #How much brighter? :D
        while val:
            #cv2.imshow("preview", frame)
            val, frame = vc.read()
            img = Image.fromarray(frame)
            img = img.resize((300,300))
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(factor)
            mode = img.mode
            size = img.size
            data = img.tobytes()
            py_img = pygame.image.frombuffer(data, size, mode)
            self.window.blit(py_img, self.pic)
            self.display.flip()
            img = img.convert("L") #Black-White
            #Change Brightness
            frame = np.array(img)#back to cv2-format.
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_shot.collidepoint(event.pos):
                        cv2.imwrite("data/image_RAW.png", frame)
                        self.btn_shot = self.window.blit(self.img_shot, self.btn_shot)
                        self.main.TextOut.addText("[J.A.R.V.I.S.]: Saved....")
                        vc.release()
                        return
                    elif self.btn_minus.collidepoint(event.pos):
                        factor -= 0.1
                        self.main.TextOut.addText("[STREAM]: DECREASED BRIGHTNESS. FACTOR: {}".format(round(factor,1)))
                    elif self.btn_plus.collidepoint(event.pos):
                        factor += 0.1
                        self.main.TextOut.addText("[STREAM]: INCREASED BRIGHTNESS. FACTOR: {}".format(round(factor,1)))

    def solve_rnd_clicked(self):
        img, solution, digit = self.main.RandomPicker.pickRandom()
        if not self.keras:
            img = img.resize((300,300))
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
            img = img.resize((300,300))
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
                imageResized = images[1][0].resize((300,300))
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
                imageResized = images[2].resize((300,300))
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
        y = 580
        for t in text:
            self.window.blit(t, (6,y))
            y -= 20
        self.display.flip()

    def drawLoader(self):
        self.window.fill([230,230,230])
        img_logo = pygame.image.load("data/images/icon_big.png")
        self.window.blit(img_logo,(150,50))
        self.textbox = pygame.draw.rect(self.window, (30,30,30), (0,474,700,600))
        pygame.draw.line(self.window, (0,25,0), (0,472),(700, 472), 3)
        self.display.flip()

    def drawMain(self):
        self.display.set_caption("A SMALL NEURONAL NETWORK!")
        #load the buttons (images!)
        self.img_shot = pygame.image.load("data/images/btn_shot.png")
        self.img_stop = pygame.image.load("data/images/btn_stop.png")

        img_solveRND = pygame.image.load("data/images/btn_solve_rnd.png")
        img_run = pygame.image.load("data/images/btn_run.png")
        img_plus = pygame.image.load("data/images/btn_plus.png")
        img_minus = pygame.image.load("data/images/btn_minus.png")
        self.window.fill([230,230,230])
        
        #White rectangle with border:
        pygame.draw.rect(self.window, [122,34,113], (48,48,303,303), 2)
        self.pic = pygame.draw.rect(self.window, [255,255,255], (50, 50,300,300))

        #Place the buttons:
        self.btn_shot = self.window.blit(self.img_shot, (400,125))
        self.btn_solveRND = self.window.blit(img_solveRND, (400,225))

        self.btn_run = self.window.blit(img_run, (550,125))

        #keras-switch:
        font = pygame.font.Font('data/arial.ttf', 14)
        text = font.render("Using Keras: ", True, (0,0,0))
        self.window.blit(text, (50,370))
        self.keras_switch = self.window.blit(self.keras_switch_false, (150,370))

        #plus and minus
        self.btn_minus = self.window.blit(img_minus, (220,370))
        self.btn_plus = self.window.blit(img_plus, (260,370))

        #Place the textfield:
        self.textbox = pygame.draw.rect(self.window, (30,30,30), (0,474,700,600))
        pygame.draw.line(self.window, (0,25,0), (0,472),(700, 472), 3)
        self.display.flip()
    


