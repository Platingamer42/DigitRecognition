#THIS CLASS ISN't NEEDED ANYMORE!
#(I still like it. Try it. alt saves and esc exits (R reloads))

import pygame, numpy, sys, scipy
from PIL import Image
from pygame import gfxdraw

def premultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255:
                r = r * a // 255
                g = g * a // 255
                b = b * a // 255
                pixels[x, y] = (r, g, b, a)

def unmultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255 and a != 0:
                r = 255 if r >= a else 255 * r // a
                g = 255 if g >= a else 255 * g // a
                b = 255 if b >= a else 255 * b // a
                pixels[x, y] = (r, g, b, a)


pygame.init()

screen = pygame.display.set_mode((100,100), pygame.HWSURFACE)
pygame.display.set_caption("Brush")

clock = pygame.time.Clock()

screen.fill((255,255,255))

b = False

while not b:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("wtf...")
            b = True
        if event.type == pygame.KEYUP:
            if event.key == 308:
                pygame.image.save(screen, "image.png")
                newImg = Image.new("L", (28,28), "white")
                pixels = newImg.load()
                img = Image.open("image.png").convert("RGBA")
                premultiply(img)
                img = img.resize((20,20))
                unmultiply(img)
                img = img.convert("L")
                px = img.load()
                #CoM:
                (X, Y) = img.size
                m = numpy.zeros((X, Y))

                for x in range(X):
                    for y in range(Y):
                        m[x, y] = px[(x, y)] != 255
                m = m / numpy.sum(numpy.sum(m))
                dx = numpy.sum(m, 1)
                dy = numpy.sum(m, 0)

                cx = int(numpy.sum(dx * numpy.arange(X)))
                cy = int(numpy.sum(dy * numpy.arange(Y)))
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        try:
                            pixels[i+4+(10-cx),j+4+(10-cy)] = px[i,j]
                        except:
                            pass
                img = newImg
                img.save("image.png", "PNG")

                print("> SAVED!")
            elif event.key == 27:
                sys.exit()
                pygame.quit()
                
            elif event.key == 114:
                screen.fill((255,255,255))
                pygame.display.flip()
    mouse_state = pygame.mouse.get_pressed()[0]
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    
    if mouse_state == 1:
        #ToDo: Create own brush - this one is shitty. #pygame.Surface.get_at bzw. set_at
        pygame.draw.line(screen, (0,0,0), (past_mouse_x, past_mouse_y), (mouse_x, mouse_y), 6)
        pygame.draw.circle(screen, (0,0,0), (mouse_x, mouse_y), 3)
    past_mouse_x = mouse_x
    past_mouse_y = mouse_y
    
    pygame.display.flip()

    clock.tick(60)
pygame.quit()

