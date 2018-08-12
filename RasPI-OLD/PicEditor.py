from PIL import Image
import numpy as np

class PicEditor:
    #returns all pictures that might contain a digit
    def getAll(self, img):
        oImage = img   
        splitted = self.split(img)
        if not splitted[0]:
            return [False]
        img = splitted[2]
        img = self.resize(img) #Height-difference, maybe.
        img = self.resize(img)
        img = self.recenter(img)
        images = [img] 

        while splitted[0]:
            next = splitted[1]
            splitted = self.split(next)

            if splitted[0]:
                img = splitted[2]
                img = self.removeWhites(splitted[2]) #Height-diff, again (maybe)
                img = self.resize(img)
                img = self.recenter(img)
                images.append(img)
            else:
                #nothing was splitted, so it's the last (rightest) one.
                next = self.resize(next)
                next = self.recenter(next)
                images.append(next)

        return [True, images, oImage]


    #returns: BOOL; RIGHT; LEFT
    #checks if there could be a image (from left to right.) 
    def split(self, img):
        img = self.removeWhites(img)
        px = np.array(img)
        found = False
        for x in range(len(px[0])):
            if (min(px[:,x]) == 255):
                found = True
                px2 = np.delete(px,[x for x in range(0, x)],1)
                px = np.delete(px,[x for x in range(x-1, len(px[0])-1)],1)
                break
        if (found):
            img = Image.fromarray(px)
            next = Image.fromarray(px2)
            return [True, next, img]
        else:
            return [False]

    def recolor(self, img):
        px = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if (px[i,j]) < 225:
                    px[i,j] = int(px[i,j] - 0.5*px[i,j])
                else:
                    px[i,j] = 255
        return img

    def removeWhites(self, img):
        px = np.array(img)
        #takeAShot [Main-class] already checks this; but if sb wants to use this method it's already safe.
        if (min(img.getdata()) == 255):
            return False
        #left:
        while min(px[:,0]) == 255:
            px = np.delete(px,0,1)
        #right:
        while min(px[:,-1]) == 255:
            px = np.delete(px,-1,1)
        #top:
        while min(px[0]) == 255:
            px = px[1:]
        #bottom:
        while min(px[-1]) == 255:
            px = px[:-1]     
        img = Image.fromarray(px)
        return img
        
    def resize(self, img):
        width, height = img.size

        #Exactly the same sizes? - NICE!
        if (width == height):
            img = img.resize((20,20), resample=Image.BICUBIC) 
        elif (width < height):
            ratio = width / height
            newWidth = round(20*ratio)
            if (newWidth == 0): #Could happen. Somehow...
                newWidth = 1
            img = img.resize((newWidth,20), resample=Image.BICUBIC)
        else:
            ratio = height / width
            newHeight = round(20*ratio)
            if newHeight == 0:
                newHeight = 1
            img = img.resize((20, newHeight), resample=Image.BICUBIC)
        return img
        
    def recenter(self, img):
        px = img.load()
        newImg = Image.new("L", (28,28), "white") #We will put "our" picture into this bad boy (later)
        pixels = newImg.load()
        #takeAShot [Main-class] already checks this; but if sb wants to use this method it's already safe.
        if min(img.getdata()) == 255:
            return False
        else:
            #cy, cx = ndimage.measurements.center_of_mass(np.array(img))
            #since scipy doesn't want to run on the PI, we have to do it ourself:
            #Changed version of: https://stackoverflow.com/questions/37519238/python-find-center-of-object-in-an-image
            (X, Y) = img.size
            m = np.zeros((X, Y))
            for x in range(X):
                for y in range(Y):
                    m[x, y] = px[(x, y)] != 255
            m = m / np.sum(np.sum(m))
            dx = np.sum(m, 1)
            dy = np.sum(m, 0)
            cx = round(np.sum(dx * np.arange(X)))
            cy = round(np.sum(dy * np.arange(Y)))
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    if (i+14-cx >= 0) and (j+14-cy >= 0) and (i+14-cx < newImg.size[0]) and (j+14-cy < newImg.size[1]): 
                    #ToDo... - IF-isn't working as it should... But why? (Out of range)
                        #width, height = img.size
                        #4 bc of the "border" and 9 bc. auf the "center"
                        pixels[i+14-cx,j+14-cy] = px[i,j]
            
            img = newImg
            return img  
            