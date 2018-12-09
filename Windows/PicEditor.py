from PIL import Image
from PIL import ImageOps
import numpy as np
from scipy import ndimage

class PicEditor:
    #returns all pictures that might contain a digit -> ALL images in the Image...
    def getAll(self, original):
        img = original.copy() # we don't change the original, please.
        img = self.removeWhites(img)

        splitted, right, left = self.split(img)
        if not splitted:
            img = self.removeWhites(img)
            img = self.resize(img)    
            img = self.recenter(img)
            #Now we can recontrast it  (for real)
            img = self.recolor(img)
            #But we have to do the other things again.
            img = self.removeWhites(img) #Height-diff, again (maybe)
            img = self.resize(img)
            img = self.recenter(img)
            return (False, [img]) #Let's pretend there is a need for a list - Otherwise we have to recode other things...
        
        img = left
        img = self.resize(img)
        recentered = self.recenter(img)
        images = [recentered] 

        while splitted:
            splitted, right, left = self.split(right)

            if splitted:
                img = left
                img = self.removeWhites(img)
                img = self.resize(img)
                img = self.recenter(img)
                #Now we can recontrast it  (for real)
                img = self.recolor(left)
                #But we have to do the other things again.
                img = self.removeWhites(img) #Height-diff, again (maybe)
                img = self.resize(img)
                img = self.recenter(img)
                images.append(img)
            else:
                #nothing was splitted, so it's the last one.
                right = self.removeWhites(right)
                right = self.resize(right)
                right = self.recenter(right)
                images.append(right)
                return (True, images)

    #checks if there could be a digit (from left to right.)
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
            return (True, next, img)
        else:
            return (False, img, None)

    def recolor(self, img):
        """
        px = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if (px[i,j]) < 225:
                    px[i,j] = int(px[i,j] - 0.5*px[i,j])
                else:
                    px[i,j] = 255
        """
        ImageOps.autocontrast(img)
        return img

    def removeWhites(self, img):
        px = np.array(img)
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
        cy, cx = ndimage.measurements.center_of_mass(np.array(img))

        cy,cx = round(cy), round(cx)

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if (i+14-cx >= 0) and (j+14-cy >= 0) and (i+14-cx < newImg.size[0]) and (j+14-cy < newImg.size[1]): 
                    pixels[i+14-cx,j+14-cy] = px[i,j]
        img = newImg
        return img


            