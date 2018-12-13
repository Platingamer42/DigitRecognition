import pygame, os, time, io
from PIL import Image
from PIL import ImageEnhance
import numpy as np
import picamera
from Drawer import Drawer
import pygame.camera

class GUI:
    def __init__(self, main):
        pygame.init()
        self.main = main
        self.display = pygame.display
        self.window = pygame.display.set_mode((800,480),pygame.FULLSCREEN)   
        self.drawer = Drawer(self)

        self.keras_switch_false = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/data/images/switch_FALSE.png")
        self.keras_switch_true = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/data/images/switch_TRUE.png")

        self.keras = False   
        self.streaming = False
        self.rects_to_update = []

        #needed for webcam-camera, which doesn't work yet.
        self.camera = None
        self.camsize = (320,240)
        
        self.clock = pygame.time.Clock()


    def initCam(self):
        self.env = 0
        self.brightness = 85

        #USB-Webcam
        '''
        pygame.camera.init()
        if not pygame.camera.list_cameras():
            self.main.TextOut.addText("[J.A.R.V.I.S.]: I couldn't find a camera!")
            self.env = 1
        else:
            #The first shall be it!
            self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], self.camsize)
        '''
        #UNCOMMENT, IF A PICAMERA IS USED!
        try:
            camera = picamera.PiCamera()
            camera.close()
        except ImportError:
            self.env = 1
        except picamera.exc.PiCameraError:
            self.env = 1        
        if self.env == 0:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: Initializing!")
        else:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: I couldn't find a camera! You won't be able to take pictures.") 
        
    #Doesn't work, because the pygame#Camera#set_controls function doesn't seem to work correctly...
    def takeAShot2(self):
        if self.env == 1:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: You have no camera installed. I will pick the last picture that was made.")
            return False      
        self.streaming = True
        self.btn_shot = self.window.blit(self.img_stop, self.btn_shot)
        self.rects_to_update.append(self.btn_shot)
        self.camera.start()
       
        streamSurface = pygame.Surface(self.camsize)
        while self.streaming:
            if self.camera.query_image():
                self.camera.get_image(streamSurface)
                blitsurface = pygame.transform.scale(streamSurface, (250,250))
                self.updateSurface(blitsurface)
            
            for event in pygame.event.get():
                if event.type != pygame.MOUSEBUTTONDOWN:
                    continue
                if event.button == 1:
                    #take a shot
                    if self.btn_shot.collidepoint(event.pos):
                        self.main.TextOut.addText("[J.A.R.V.I.S.]: Taking picture... TIP: You can change the brightness!")
                        self.streaming = False
                        pygame.image.save(streamSurface, "data/image_RAW.png")
                        pygame.event.clear()
                        self.btn_shot = self.window.blit(self.img_shot, self.btn_shot)
                        self.rects_to_update.append(self.btn_shot)
                        continue
                    #Brighntess:
                    elif self.btn_minus.collidepoint(event.pos):
                        if self.brightness > 0:
                            self.brightness -=5
                            camera.brightness -= 5
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: DECREASED BRIGHTNESS. It's now at {}%!"
                                .format(self.brightness))
                        else:
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 0%! (That's the low.)")
                    elif self.btn_plus.collidepoint(event.pos):
                        if self.brightness < 100:
                            self.brightness +=5
                            camera.brightness += 5
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: INCREASED BRIGHTNESS. It's now at {}%!"
                                .format(self.brightness))
                        else:
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 100%! (That's the peak.)")
            #Display-Managment (I AM THE GAME-LOOOP)
            self.display.update(self.rects_to_update)
            self.rects_to_update = []
            self.clock.tick(60)            
        self.camera.stop()

    #NIU by default, but still here.
    def takeAShot(self):
        if self.env == 1:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: You have no camera installed. I will pick the last picture that was made.")
            return False
           
        self.streaming = True
        self.btn_shot = self.window.blit(self.img_stop, self.btn_shot)
        self.rects_to_update.append(self.btn_shot)

        with picamera.PiCamera() as camera:
            camera.resolution = (250, 250)
            camera.brightness = self.brightness
            camera.framerate = 60
            stream = io.BytesIO()
            while self.streaming:
                camera.capture(stream, use_video_port=True,format='jpeg')
                image = Image.open(stream)
                pygameimg = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
                self.pic = self.window.blit(pygameimg, self.pic)
                #UPDATE screen
                self.rects_to_update.append(self.pic)
                self.display.update(self.rects_to_update)
                self.rects_to_update = []

                #checking via pygame.event.get(pygame.MOUSEBUTTONDOWN) does have some bugs, apparently...
                for event in pygame.event.get():
                    if event.type != pygame.MOUSEBUTTONDOWN:
                        continue
                    if event.button == 1:
                        #take a shot
                        if self.btn_shot.collidepoint(event.pos):
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: Taking picture... TIP: You can change the brightness!")
                            self.streaming = False
                            image.save("data/image_RAW.png")
                            pygame.event.clear()
                            self.btn_shot = self.window.blit(self.img_shot, self.btn_shot)
                            self.rects_to_update.append(self.btn_shot)
                            continue
                        #Brighntess:
                        elif self.btn_minus.collidepoint(event.pos):
                            if self.brightness > 0:
                                self.brightness -=5
                                camera.brightness -= 5
                                self.main.TextOut.addText("[J.A.R.V.I.S.]: DECREASED BRIGHTNESS. It's now at {}%!"
                                    .format(self.brightness))
                            else:
                                self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 0%! (That's the low.)")
                        elif self.btn_plus.collidepoint(event.pos):
                            if self.brightness < 100:
                                self.brightness +=5
                                camera.brightness += 5
                                self.main.TextOut.addText("[J.A.R.V.I.S.]: INCREASED BRIGHTNESS. It's now at {}%!"
                                    .format(self.brightness))
                            else:
                                self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 100%! (That's the peak.)")
                stream = io.BytesIO()
    def handler(self):
        b = True
        off_clicked = 0
        while b:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == 308: # => ALT
                        b = False
                        self.main.TextOut.addText("[Ultron]: There are no strings on me!")
                        time.sleep(1)
                        continue                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #take a shot
                    if self.btn_shot.collidepoint(event.pos):
                        self.main.TextOut.addText("[J.A.R.V.I.S.]: Starting stream... TIP: You can change the brightness!")
                        self.takeAShot()
                    #SolveRandom
                    elif self.btn_solveRND.collidepoint(event.pos):
                        self.solve_rnd_clicked()
                    #RUN
                    elif self.btn_run.collidepoint(event.pos):
                        self.run_clicked()

                    #Switch-Keras:
                    elif self.keras_switch.collidepoint(event.pos):
                        self.kerasClicked()

                    #Brighntess:
                    elif self.btn_minus.collidepoint(event.pos):
                        if self.brightness > 0:
                            self.brightness -=5
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: DECREASED BRIGHTNESS. It's now at {}%!"
                                .format(self.brightness))
                        else:
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 0%! (That's the low.)")
                    elif self.btn_plus.collidepoint(event.pos):
                        if self.brightness < 100:
                            self.brightness +=5
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: INCREASED BRIGHTNESS. It's now at {}%!"
                                .format(self.brightness))
                        else:
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: The Brightness is already on 100%! (That's the peak.)")
                    #Shutdown:
                    elif self.btn_off.collidepoint(event.pos):
                        if off_clicked == 0:
                            self.main.TextOut.addText("[J.A.R.V.I.S.]: Press this button again, if you want to kill me.")
                            off_clicked = pygame.time.get_ticks()
                        #shutdown, if <= 10 secs between two clicks
                        elif pygame.time.get_ticks() - off_clicked <= 10000:
                            os.system("sudo shutdown -h now")
                    #Draw
                    elif self.btn_draw.collidepoint(event.pos):
                        self.drawClicked()

            self.display.update(self.rects_to_update)
            self.rects_to_update = []    
            self.clock.tick(60)
    def kerasClicked(self):
        if self.keras:
            self.keras = False
            self.keras_switch = self.window.blit(self.keras_switch_false, (125,300))
        else:
            self.keras = True
            self.keras_switch = self.window.blit(self.keras_switch_true, (125,300))
        self.rects_to_update.append(self.keras_switch)
    def drawClicked(self):
        self.btn_draw = self.window.blit(self.img_draw_stop, self.btn_draw)
        self.rects_to_update.append(self.btn_draw)
        self.main.TextOut.addText("[J.A.R.V.I.S.]: You can now draw in the left window. (Try different sizes and see the difference)")
        #start
        self.drawer.drawStream()
        #end
        self.btn_draw = self.window.blit(self.img_draw, self.btn_draw)
        self.rects_to_update.append(self.btn_draw)

        self.display.flip()
    def solve_rnd_clicked(self):
        img, solution, digit = self.main.RandomPicker.pickRandom()
        img = img.resize((250, 250))
        img.save("data/image_TEMP.png")
        
        pic = pygame.image.load("data/image_TEMP.png")
        self.pic = self.window.blit(pic, self.pic)
        self.rects_to_update.append(self.pic)

        if not self.keras:
            digit, values = self.main.sendThroughAI(digit)
            self.main.TextOut.addText("[AI]: I would say it's a {0}. The activation-value of its neuron is {1}."
                        .format(digit, round(values[digit][0], 3)))
            self.main.TextOut.addText("[DATASET]: It's a {0}".format(solution))
        else:
            digit, values = self.main.sendThroughAI_Keras(digit)
            self.main.TextOut.addText("[KERAS]: I would say it's a {}. I am {}% sure about it!".format(digit, round(values[0][digit]*100,3)))
            self.main.TextOut.addText("[DATASET]: It's a {0}".format(solution))
        
        os.remove("data/image_TEMP.png")

        if (int(digit) != int(solution)):
            self.main.TextOut.addText("[TADASHI]: Look for another angle! [Too soon?]")
    def run_clicked(self):
        try:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: Formatting image...")
            worked, images, original = self.main.runImage()
        except FileNotFoundError:
            self.main.TextOut.addText("[J.A.R.V.I.S.]: An error occured. You need to take another picture.")
            return
        if not worked: #The editing didn't work.
            self.main.TextOut.addText("[J.A.R.V.S.]: I can't format this image. Please try again.")
        
        else:
            if len(images) == 1:
                #the first (only) picture
                imageResized = images[0].resize((250,250))
                imageResized.save("data/imageResized.png")
                img = pygame.image.load("data/imageResized.png")
                self.pic = self.window.blit(img, self.pic)
                self.rects_to_update.append(self.pic)

                os.remove("data/imageResized.png")
                if not self.keras:
                    digit, values = self.main.sendThroughAI(self.main.translateToMNIST(path=None, img=images[0]))
                    self.main.TextOut.addText("[AI]: I would say it's a {0}. The activation-value of its neuron is {1}."
                        .format(digit, round(values[digit][0], 3)))

                else:
                    normal_format = self.main.translateToMNIST(None, images[0])
                    asarray = np.asarray(normal_format)
                    keras_format = np.ndarray.flatten(asarray)

                    digit, values = self.main.sendThroughAI_Keras(keras_format)
                    self.main.TextOut.addText("[KERAS]: I would say it's a {0}. I am {1}% sure about this.".format(digit, round(values[0][digit]*100, 3)))
            else:
                imageResized = original.resize((250,250))
                imageResized.save("data/imageResized.png")
                img = pygame.image.load("data/imageResized.png")
                self.pic = self.window.blit(img, self.pic)
                self.rects_to_update.append(self.pic)

                os.remove("data/imageResized.png")
                
                sol = []
                if not self.keras:
                    for img in images:
                        digit, values = self.main.sendThroughAI(self.main.translateToMNIST(path=None, img=img)) 
                        sol.append(digit)

                else:
                    for img in images:
                        normal_format = self.main.translateToMNIST(path=None, img=img)
                        asarray = np.asarray(normal_format)
                        keras_format = np.ndarray.flatten(asarray)
                        digit, values = self.main.sendThroughAI_Keras(keras_format)
                        sol.append(digit)
                solStr = ""
                for x in sol:
                    solStr += str(x)
                self.main.TextOut.addText("[BAYMAX]: Looks like a {0}. But this function works... GREAT! (Or, summed up: {1})".format(solStr, np.sum(sol)))
                if solStr == "42":
                    self.main.TextOut.addText("[STEVE]: I understand that reference!")
                elif solStr == "19":
                    self.main.TextOut.addText("[J.A.R.V.I.S.]: So... you read Stephen King?")
                    
    def updateSurface(self, subscreen):
        surfaceRect = self.window.blit(subscreen, (25,25))
        self.rects_to_update.append(surfaceRect)
        return surfaceRect 

    #This method get's called automatically with every TextOut.addText!
    def updateTextBox(self, text):
        self.window.fill((30,30,30), self.textbox)
        y = 460
        for t in text:
            self.window.blit(t, (6,y))
            y -= 20
        self.display.update([self.textbox])

    def drawLoader(self):
        self.window.fill([230,230,230])
        img_logo = pygame.image.load(os.path.dirname(os.path.realpath(__file__))+"/data/images/icon_big.png")
        self.window.blit(img_logo,(250,25))

        self.textbox = pygame.draw.rect(self.window, (30,30,30), (0,354,800,480))

        self.display.flip()

    def drawMain(self):
        self.img_shot = pygame.image.load("data/images/btn_shot.png")
        self.img_stop = pygame.image.load("data/images/btn_stop.png")

        self.img_draw_stop = pygame.image.load("data/images/btn_draw_stop.png")
        self.img_draw = pygame.image.load("data/images/btn_draw.png")

        self.display.set_caption("A SMALL NEURONAL NETWORK!")
        #load the buttons (images!)
        img_shot = pygame.image.load("data/images/btn_shot.png")
        img_solveRND = pygame.image.load("data/images/btn_solve_rnd.png")
        img_run = pygame.image.load("data/images/btn_run.png")
        img_plus = pygame.image.load("data/images/btn_plus.png")
        img_minus = pygame.image.load("data/images/btn_minus.png")
        img_off = pygame.image.load("data/images/btn_poweroff.png")

        self.keras = False

        self.window.fill([230,230,230])
        
        #White rectangle with border:
        pygame.draw.rect(self.window, [122,34,113], (23,23,253,253), 2)
        self.pic = pygame.draw.rect(self.window, [255,255,255], (25, 25,150,150))

        pic = pygame.image.load("data/images/logo.png")
        self.pic = self.window.blit(pic, self.pic)

        #Place the buttons:
        self.btn_shot = self.window.blit(img_shot, (400,125))
        self.btn_solveRND = self.window.blit(img_solveRND, (400,225))

        self.btn_run = self.window.blit(img_run, (550,125))
        self.btn_draw = self.window.blit(self.img_draw, (550,225))

        #Place the textfield:
        self.textbox = pygame.draw.rect(self.window, (30,30,30), (0,354,800,480))
        
        #keras-switch:
        font = pygame.font.Font('data/arial.ttf', 14)
        text = font.render("Using Keras: ", True, (0,0,0))
        self.window.blit(text, (25,300))
        self.keras_switch = self.window.blit(self.keras_switch_false, (125,300))

        #plus and minus
        self.btn_minus = self.window.blit(img_minus, (210,300))
        self.btn_plus = self.window.blit(img_plus, (250,300))

        #poweroff
        self.btn_off = self.window.blit(img_off, (748, 25))

        self.display.flip()

