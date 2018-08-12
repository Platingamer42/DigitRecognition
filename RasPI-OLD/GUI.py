import pygame, os, time
from PIL import Image
import numpy as np

class GUI:
    def __init__(self, main):
        pygame.init()
        self.main = main
        self.clock = pygame.time.Clock()
        self.display = pygame.display
        self.display.set_icon(pygame.image.load("data/images/icon.png")) #No one will ever see this, but idc.
        self.window = pygame.display.set_mode((800,480), pygame.HWSURFACE|pygame.FULLSCREEN)   
            
    def handler(self):
        b = True
        while b:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == 308: # => ALT
                        b = False
                        self.main.TextOut.addText("[Ultron]: There are no strings on me!")
                        time.sleep(2)
                        continue                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                    b = False
                    self.main.TextOut.addText("[Ultron]: There are no strings on me!")
                    time.sleep(2)
                    continue

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #take a shot
                    if self.btn_shot.collidepoint(event.pos):
                        self.main.takeAShot()
                        try:
                            image = Image.open("data/image_RAW.png")
                            imageResized = image.resize((150,150))
                            imageResized.save("data/imageResized.png")
                            pic = pygame.image.load("data/imageResized.png")
                            self.pic = self.window.blit(pic, self.pic)
                            self.display.flip()
                            os.remove("data/imageResized.png")
                        except FileNotFoundError:
                            self.main.TextOut.addText("[J.A.R.V.I.S.] An error occured. You need to take another picture.")
                    #SolveRandom
                    elif self.btn_solveRND.collidepoint(event.pos):
                        self.solve_rnd_clicked()
                    #RUN
                    elif self.btn_run.collidepoint(event.pos):
                        self.run_clicked()

    def solve_rnd_clicked(self):
        img, solution, digit = self.main.RandomPicker.pickRandom()
        
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
                digit, values = self.main.sendThroughAI(self.main.translateToMNIST(None, images[1][0]))
                self.main.TextOut.addText("[AI]: I would say it's a {0}. The activation-value of its neuron is {1}."
                        .format(digit, round(values[digit][0], 3)))
            else:
                imageResized = images[2].resize((150,150))
                imageResized.save("data/imageResized.png")
                img = pygame.image.load("data/imageResized.png")
                self.pic = self.window.blit(img, self.pic)
                self.display.flip()
                os.remove("data/imageResized.png")
                
                sol = []
                for img in images[1]:
                    digit, values = self.main.sendThroughAI(self.main.translateToMNIST(path=None, img=img)) 
                    sol.append(digit)
                solStr = ""
                for x in sol:
                    solStr += str(x)
                self.main.TextOut.addText("[AI]: Looks like a {0}. But this function works... GREAT! (Or, summed up: {1} [@Schlögl...])".format(solStr, np.sum(sol)))

    def updateTextBox(self, text):
        self.window.fill((30,30,30), self.textbox)
        y = 460
        for t in text:
            self.window.blit(t, (6,y))
            y -= 20
        self.display.flip()

    def drawLoader(self):
        self.window.fill([230,230,230])
        img_logo = pygame.image.load("data/images/icon_big.png")
        self.window.blit(img_logo,(250,25))

        self.textbox = pygame.draw.rect(self.window, (30,30,30), (0,354,800,480))

        self.display.flip()

    def drawMain(self):
        self.display.set_caption("A SMALL NEURONAL NETWORK!")
        #load the buttons (images!)
        img_shot = pygame.image.load("data/images/btn_shot.png")
        img_solveRND = pygame.image.load("data/images/btn_solve_rnd.png")
        img_run = pygame.image.load("data/images/btn_run.png")

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

        self.display.flip()
    


