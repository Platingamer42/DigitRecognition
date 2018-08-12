import pygame

class TextOut:
    def __init__(self, GUI):
        self.GUI = GUI
        self.text = []
        pygame.font.init()
        self.font = pygame.font.Font('data/arial.ttf', 14)

    def addText(self, text):
        #Caching the rendered font, since it's quite a slow function.
        if len(self.text) < 6:
            self.text.append(self.font.render(text, True, (0,255,0)))
        else:
            self.text = self.text[1:]
            self.text.append(self.font.render(text, True, (0,255,0)))
        
        #We should reverse the list! YOU COULD MAKE A RELIGION OUT OF THIS.
        self.GUI.updateTextBox(self.text[::-1])
    def reset(self):
        self.text = []