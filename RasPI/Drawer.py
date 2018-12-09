import pygame

class Drawer:
    def __init__(self, gui):
        self.pygame = pygame
        self.GUI = gui

    def drawStream(self):
        screen = pygame.Surface((250,250))
        screen.fill((255,255,255))
        self.drawRect = self.GUI.updateDrawer(screen)
        pygame.event.clear()
        past_mouse_x, past_mouse_y = 0, 0
        drawing = False
        b = False
        clock = pygame.time.Clock()
        while not b:  
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:    
                    self.pygame.image.save(screen, "data/image_RAW.png")
                    self.GUI.run_clicked()  
                    self.GUI.updateDrawer(screen)
                    drawing = False
               
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    
                    #STOPDRAW
                    if self.GUI.btn_draw.collidepoint(event.pos):
                        self.GUI.run_clicked()
                        pygame.event.clear()
                        return
                    #KERAS
                    if self.GUI.keras_switch.collidepoint(event.pos):
                        self.GUI.kerasClicked()
                    elif self.drawRect.collidepoint(event.pos):
                        mouse_x = pygame.mouse.get_pos()[0] - 25
                        mouse_y = pygame.mouse.get_pos()[1] - 25
                        past_mouse_x, past_mouse_y = mouse_x, mouse_y
                        drawing = True 
            if drawing:
                mouse_state = pygame.mouse.get_pressed()[0]
            
                #shifting!
                mouse_x = pygame.mouse.get_pos()[0] - 25
                mouse_y = pygame.mouse.get_pos()[1] - 25
    
                if mouse_state == 1:
                    #ToDo: Create own brush
                    pygame.draw.line(screen, (0,0,0), (past_mouse_x, past_mouse_y), (mouse_x, mouse_y), 8)
                    pygame.draw.circle(screen, (0,0,0), (mouse_x, mouse_y), 4)
                past_mouse_x, past_mouse_y = mouse_x, mouse_y
                self.GUI.updateDrawer(screen)
                
            self.GUI.display.update(self.GUI.rects_to_update)
            self.GUI.rects_to_update = []
            clock.tick(60)
    
            
